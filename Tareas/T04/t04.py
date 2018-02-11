from random import randrange, choice, random, expovariate, uniform, triangular
from my_random import weighted_choice
import csv
from bernoulli_event import bernoulli
import matplotlib.pyplot as plt

class AdvancedProgramming:
    '''
    Class to control the course. It controls all the events in a semester
    '''
    dificulty = [2, 2, 3, 5, 7, 10, 7, 9, 1, 6, 6, 5]

    def __init__(self, percentage_progress_tarea_mail, month_party, month_football):
        self.integrantes_filename = 'integrantes.csv'
        self.sections = {}
        self.coordinator = None
        self.teacher_assistants = []
        self.task_assistants = []
        self.percentaje_progress_tarea_mail = percentage_progress_tarea_mail
        self.month_party = month_party
        self.month_football = month_football
        self.events_list = []
        self.corte_agua_days = []
        self.football_days = []
        self.tareas_publication_days = []
        self.controles_days = []
        self.harder_tarea = False
        self.fechas_tareas = []
        self.fechas_publicacion_notas_act = []
        self.fechas_ayudantias = []
        self.fechas_catedras = []

    @property
    def controles_weeks(self):
        return [int(day / 7) for day in self.controles_days]

    @property
    def corte_agua_weeks(self):
        return [int(day / 7) for day in self.corte_agua_days]

    @property
    def all_students(self):
        everyone = []
        for section in self.sections.values():
            everyone += section.students

        return everyone

    @property
    def active_students(self):
        '''Returns a list with the current active students '''
        return [student for student in self.all_students if student.active]

    @property
    def dataframe_proms(self):
        '''Returns a dictionary with all the average scores per evaluation '''
        df = {'MATERIA': [i for i in range(12)]}
        df['PROM CONTROLES'] = []
        df['PROM ACT'] = []
        df['PROM TAREAS'] = []

        for week in range(0, 12):
            notas_controles = [student.notas_controles[week] for student in self.active_students if week in student.notas_controles]
            notas_actividades = [student.notas_act[week] for student in self.active_students if week in student.notas_act]
            notas_tareas = [student.notas_tareas[week] for student in self.active_students if week in student.notas_tareas]
            try:
                control_avg = sum(notas_controles) / len(notas_controles)
            except ZeroDivisionError:
                control_avg = 'NaN'
            try:
                act_avg = sum(notas_actividades) / len(notas_actividades)
            except ZeroDivisionError:
                act_avg = 'NaN'
            try:
                tareas_avg = sum(notas_tareas) / len(notas_tareas)
            except ZeroDivisionError:
                tareas_avg = 'NaN'
            df['PROM CONTROLES'].append(control_avg)
            df['PROM ACT'].append(act_avg)
            df['PROM TAREAS'].append(tareas_avg)
        return df

    @property
    def list_tuples_prom(self):
        '''Returns a list of tuples with : (materia_n, promedio_n) '''
        list_tuples = []
        for row in self.dataframe_proms['MATERIA']:
            Sum = 0
            n = 0
            if self.dataframe_proms['PROM CONTROLES'][row] != 'NaN':
                Sum += self.dataframe_proms['PROM CONTROLES'][row]
                n += 1
            if self.dataframe_proms['PROM ACT'][row] != 'NaN':
                Sum += self.dataframe_proms['PROM ACT'][row]
                n += 1
            if self.dataframe_proms['PROM TAREAS'][row] != 'NaN':
                Sum += self.dataframe_proms['PROM TAREAS'][row]
                n += 1
            avg = Sum / n
            list_tuples.append((row, avg))

    def add_person(self, person, section_number):
        '''Adds a person depending on their rol '''
        if section_number == '':
            if isinstance(person, Coordinator):
                self.coordinator = person
            elif isinstance(person, TeacherAssistant):
                if person not in self.teacher_assistants:
                    self.teacher_assistants.append(person)
            elif isinstance(person, TaskAssistant):
                if person not in self.task_assistants:
                    self.task_assistants.append(person)
        else:
            if section_number in self.sections:
                section = self.sections[section_number]
            else:
                section = Section(section_number)
                self.sections[section_number] = section
            if isinstance(person, Student):
                section.add_student(person)
            elif isinstance(person, Proffessor):
                section.add_proffesor(person)

    def simulate_meeting_day(self, time_day):
        '''It simulates a meeting day with a proffesor '''
        print('[{}] Dia de atencion de profesores'.format(time_day))
        time_week = int(time_day / 7)
        for section in self.sections.values():
            profe = section.proffesor
            for student in section.students:
                student.visit_proffesor(time_day, profe)
            if time_week in self.corte_agua_weeks:
                capacity = 6
            else:
                capacity = 10
            profe.atender_students(time_day, capacity)
        self.events_list.append(('meeting day', time_day + 7))

    def simulate_corte_agua(self, time_day):
        '''Simulates a corte de agua. Adds the date to a list, so the teacher's capacity is limited '''
        self.events_list.append(('corte agua', int(time_day + expovariate(1 / 21))))
        time_week = int(time_day / 7)
        if len(self.corte_agua_weeks) != 0:
            if time_week == self.corte_agua_weeks[-1]:
                return
        else:
            print('[{}] Hubo corte de agua'.format(time_day))
            self.corte_agua_days.append(time_day)

    def simulate_party(self, time_day):
        '''Simulates party '''
        self.events_list.append(('party', int(time_day + expovariate(1 / 30))))
        went_to_this_party = []
        for i in range(min(len(self.active_students), 50)):
            s = choice(self.active_students)
            s.go_to_party(time_day)
            while s in went_to_this_party:
                s = choice(self.active_students)
            went_to_this_party.append(s)
        print('[{}] Hubo una fiesta. Fueron {} alumnos'.format(time_day, min(len(self.active_students), 50)))

    def simulate_football(self, time_day):
        '''Simulates a football event. Changes the harder tarea atribute to true '''
        self.events_list.append(('football', int(time_day + expovariate(1 / 70))))
        n_students = round(0.8 * len(self.active_students))
        for i in range(n_students):
            student = choice(self.active_students)
            student.watch_football(time_day)
        self.harder_tarea = True
        self.football_days.append(time_day)
        print('[{}] Hubo una partido de football. Fueron {} alumnos'.format(time_day, n_students))

    def simulate_actividad(self, time_day):
        '''Simulates an activity and add the publication event to the list '''
        time_week = int(time_day / 7)
        exigencia = 7 + randrange(1, 6) / AdvancedProgramming.dificulty[time_week]
        notas_act = {}
        for student in self.active_students:
            nota = student.rendir_evaluacion(time_day, 'actividad', exigencia)
            notas_act[student.id] = nota
        self.events_list.append(('entrega notas actividad', time_day + 14, notas_act))
        print('[{}] Hubo una actividad. Fueron {} alumnos'.format(time_day, len(self.active_students)))

    def simulate_control(self, time_day):
        '''Simulates a control and gets the grades. These grades will be published in their corresponding time '''
        time_week = int(time_day / 7)
        if len(self.controles_weeks) != 0:
            if time_week == self.controles_weeks[-1] + 1:
                return
        if len(self.controles_days) > 5:
            return
        else:
            self.controles_days.append(time_day)
            time_week = int(time_day / 7)
            exigencia = 7 + randrange(1, 6) / AdvancedProgramming.dificulty[time_week]
            notas_controles = {}
            for student in self.active_students:
                nota = student.rendir_evaluacion(time_day, 'control', exigencia)
                notas_controles[student.id] = nota
            self.events_list.append(('entrega notas control', time_day + 14, notas_controles))
            print('[{}] Hubo una control. Fueron {} alumnos'.format(time_day, len(self.active_students)))

    def simulate_exam(self, time_day):
        '''Simulates the exam and adds the grades publication event to the events list '''
        materias_ordenadas = [tup[0] for tup in sorted(self.list_tuples_prom, key=lambda x: x[1])]
        materias_to_evaluate = materias_ordenadas[0: 6] + materias_ordenadas[:-2]
        exigencias = [7 + uniform(1, 5) / AdvancedProgramming.dificulty[i] for i in materias_to_evaluate]
        notas_exam = {}
        for student in self.active_students:
            nota = student.rendir_examen(time_day, materias_to_evaluate, exigencias)
            notas_exam[student.id] = nota
        self.events_list.append('entrega notas examen', time_day + 14, notas_exam)
        print('[{}] Hubo un examen. Fueron {} alumnos'.format(time_day, len(self.active_students)))

    def simulate_realizar_tarea(self, time_day, exigencia):
        '''Simulates the submit of a tarea. It does not include the sending mails process '''
        if len(self.fechas_tareas) >= 5:
            return
        notas_tareas = {}
        fecha_publicacion = self.fechas_tareas[-1]
        for student in self.active_students:
            nota = student.rendir_evaluacion(time_day, 'tarea', exigencia, fecha_publicacion)
            notas_tareas[student.id] = nota
        self.events_list.append(('entrega notas tareas', time_day + 14, notas_tareas))
        print('[{}] Los alumnos subieron su tarea {}. Fueron {} alumnos'.format(time_day, len(self.fechas_tareas) - 1, len(self.active_students)))

    def publicar_notas(self, time_day, notas, eval_name):
        '''It sets the grades on the active students. '''
        time_week = int(time_day / 7)
        for i, nota in notas.items():
            student = [s for s in self.all_students if s.id == i].pop()
            if eval_name == 'actividad':
                student.notas_act[time_week] = nota
                student.update_confidence(time_day, n_a=nota)
            elif eval_name == 'control':
                student.notas_controles[time_week] = nota
                student.update_confidence(time_day, n_c=nota)
            elif eval_name == 'examen':
                student.notas_exam[time_week] = nota
            elif eval_name == 'tarea':
                student.notas_tareas[time_week - 2] = nota
                student.update_confidence(time_day, n_t=nota)
        if eval_name == 'actividad':
            self.fechas_publicacion_notas_act.append(time_day)
            if len(self.fechas_publicacion_notas_act) == 4:
                self.simulate_bota_ramos(time_day)

        print('[{}] Se publicaron notas de {}. Fueron {} alumnos'.format(time_day, eval_name, len(self.active_students)))

    def simulate_publicacion_tarea(self, time_day):
        '''Simulates the meeting to set the exigencia and then it publishes the tarea. '''
        if len(self.fechas_tareas) >= 5:
            return
        time_week = int(time_day / 7)
        exigencia = 7 + randrange(1, 6) / AdvancedProgramming.dificulty[time_week]
        if self.harder_tarea:
            exigencia *= exigencia
            self.harder_tarea = False
        self.fechas_tareas.append(time_day)
        self.events_list.append(('publicacion tarea', time_day + 14))
        self.events_list.append(('realizar tarea', time_day + 14, exigencia))
        print('[{}] Se publica la tarea {}. Fueron {} alumnos'.format(time_day, len(self.fechas_tareas), len(self.active_students)))

    def simulate_catedra(self, time_day):
        '''Simulate a catedra. First, updates the programming level, then simulates a control, then the tips and finally the actividad '''
        if len(self.fechas_catedras) >= 12:
            return
        self.update_programming_level(time_day)
        self.fechas_catedras.append(time_day)
        time_week = int(time_day / 7)
        if time_week <= 11:
            self.events_list.append(('catedra', time_day + 7))

        if bool(bernoulli(0.5)):
            self.simulate_control(time_day)

        for student in self.active_students:
            if bool(bernoulli(0.5)):
                student.listen_tip(time_day)

        i = 0
        while i <= 600:
            student = choice(self.active_students)
            n_questions = round(triangular(1, 10, 3))
            i += n_questions
            student.ask_questions(time_day, n_questions)

        self.simulate_actividad(time_day)
        print('[{}] Hubo una catedra. Fueron {} alumnos'.format(time_day, len(self.active_students)))

    def simulate_ayudantia(self, time_day):
        '''Checks if the ayudante is pro in a subject. If it is, then gives tip to everyone. '''
        if len(self.fechas_ayudantias) >= 12:
            return
        self.fechas_ayudantias.append(time_day)
        time_week = int(time_day / 7)
        ayudantes_today = [choice(self.teacher_assistants) for i in range(2)]
        ayu_1 = ayudantes_today[0]
        ayu_2 = ayudantes_today[1]
        if time_week in ayu_1.skilled_subjects:
            for student in self.sections['1'].students + self.sections['3'].students:
                student.listen_ayudantia(time_day)
        if time_week in ayu_2.skilled_subjects:
            for student in self.sections['2'].students:
                student.listen_ayudantia(time_day)
        self.events_list.append(('ayudantia', time_day + 7))
        print('[{}] Hubo una ayudantia. Fueron {} alumnos'.format(time_day, len(self.active_students)))

    def simulate_bota_ramos(self, time_day):
        '''Simulates the bota de ramos event. But the s value was changed. '''
        n = 0
        for student in self.active_students:
            s = student.confidence * 0.8 + student.promedio * 0.2
            if s < 2:
                student.active = False
                n += 1
        print('[{}] Hubo una bota de ramos. Botaron {} alumnos'.format(time_day, n))

    def update_programming_level(self, time_day):
        '''Updates programming level of every student '''
        for student in self.active_students:
            student.update_programming_level(time_day)

    def run(self):
        '''Run the simuation. It starts with some base events. '''
        time_day = -1
        self.events_list.append(('ayudantia', time_day + 5))
        self.events_list.append(('meeting day', time_day + 6))
        self.events_list.append(('catedra', time_day + 7))
        self.events_list.append(('publicacion tarea', time_day + 14))
        self.events_list.append(('football', int(time_day + expovariate(1 / 70))))
        self.events_list.append(('party', int(time_day + expovariate(1 / 30))))
        self.events_list.append(('corte agua', int(time_day + expovariate(1 / 21))))
        self.events_list.sort(key=lambda x: x[1])

        while len(self.events_list) != 0:
            event_tuple = self.events_list[0]
            self.events_list = self.events_list[1:]
            event = event_tuple[0]
            time_day = event_tuple[1]
            # if int(time_day / 7) > 11:
            #     self.simulate_exam(time_day)
            if event == 'catedra':
                self.simulate_catedra(time_day)
            elif event == 'ayudantia':
                self.simulate_ayudantia(time_day)
            elif event == 'meeting day':
                self.simulate_meeting_day(time_day)
            elif event == 'football':
                self.simulate_football(time_day)
            elif event == 'party':
                self.simulate_party(time_day)
            elif event == 'corte agua':
                self.simulate_corte_agua(time_day)
            elif event == 'entrega notas actividad':
                notas = event_tuple[2]
                self.publicar_notas(time_day, notas, 'actividad')
            elif event == 'entrega notas control':
                notas = event_tuple[2]
                self.publicar_notas(time_day, notas, 'control')
            elif event == 'entrega notas examen':
                notas = event_tuple[2]
                self.publicar_notas(time_day, notas, 'examen')
                print('FIN SIMULACION')
                break
            elif event == 'entrega notas tareas':
                notas = event_tuple[2]
                self.publicar_notas(time_day, notas, 'tarea')
            elif event == 'realizar tarea':
                exigencia = event_tuple[2]
                self.simulate_realizar_tarea(time_day, exigencia)
            elif event == 'publicacion tarea':
                self.simulate_publicacion_tarea(time_day)

            if 'entrega notas control' not in [i[0] for i in self.events_list] and\
                'entrega notas actividad' not in [i[0] for i in self.events_list] and\
                'entrega notas tareas' not in [i[0] for i in self.events_list] and\
                    time_day > 80:
                    self.simulate_exam(time_day + 5)

            self.events_list.sort(key=lambda x: x[1])


class Section:
    '''It has students and a professor '''
    def __init__(self, section_number):
        self.students = []
        self.proffesor = None
        self.section_number = section_number

    def add_student(self, student):
        if student not in self.students:
            self.students.append(student)

    def add_proffesor(self, proffesor):
        if self.proffesor is None:
            self.proffesor = proffesor


class Person:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Coordinator(Person):
    '''Mavrakis '''
    def __init__(self, name):
        super().__init__(name)


class Proffessor(Person):
    '''In charge of a section '''
    def __init__(self, name):
        super().__init__(name)
        self.cola = []

    def atender_students(self, time_day, capacity):
        for i in range(min(len(self.cola), capacity)):
            student = choice(self.cola)
            self.cola.remove(student)
            student.meeting_days.append(time_day)
        self.cola.clear()


class TeacherAssistant(Person):
    def __init__(self, name):
        super().__init__(name)
        self.skilled_subjects = [randrange(0, 12) for i in range(3)]


class TaskAssistant(Person):
    def __init__(self, name):
        super().__init__(name)


class Student(Person):
    '''Class to simulate a student '''
    nota_esperada = {(1.1, 3.9): [(0, 2), (0, 3), (0, 1), (0, 2), (0, 3), (0, 4), (0, 3), (0, 2), (0, 1), (0, 4), (0, 2), (0, 2)],
                     (4.0, 5.9): [(3, 4), (4, 6), (2, 4), (3, 5), (4, 7), (5, 7), (4, 6), (3, 5), (2, 4), (5, 7), (3, 5), (3, 7)],
                     (6.0, 6.9): [(5, 6), (7, 7), (5, 6), (6, 7), (8, 8), (8, 9), (7, 8), (6, 7), (5, 6), (8, 9), (6, 7), (8, 8)],
                     (7.0, 7.0): [(7, ), (8, ), (7, ), (8, ), (9, ), (10, ), (9, ), (8, ), (7, ), (10, ), (8, ), (9, )]}

    dificulty = [2, 2, 3, 5, 7, 10, 7, 9, 1, 6, 6, 5]

    def __init__(self, name, prob_40_credits, prob_50_credits, prob_55_credits,
                 prob_60_credits, prob_visit_proffesor, initial_level_confidence_inf, initial_level_confidence_sup):
        super().__init__(name)
        self.initial_confidence = randrange(initial_level_confidence_inf, initial_level_confidence_sup + 1)
        choices = [(40, prob_40_credits), (50, prob_50_credits), (55, prob_55_credits),
                   (60, prob_60_credits)]
        self.total_credits = weighted_choice(choices)
        if self.total_credits == 40:
            self.horas_totales_semanas = {i: randrange(10, 26) for i in range(0, 12)}
        elif self.total_credits == 50:
            self.horas_totales_semanas = {i: randrange(10, 16) for i in range(0, 12)}
        elif self.total_credits == 55:
            self.horas_totales_semanas = {i: randrange(5, 16) for i in range(0, 12)}
        elif self.total_credits == 60:
            self.horas_totales_semanas = {i: randrange(10, 11) for i in range(0, 12)}
        self.horas_estudiadas = {i: 0 for i in range(0, 12)}
        self.horas_tareas = {i: 0 for i in range(0, 12)}
        self.manejo_contenidos = {i: 0 for i in range(0, 12)}
        self.personality = choice(['efficient', 'artistic', 'theoretical'])
        self.programming_levels_dict = {i: 0 for i in range(0, 12)}
        self.prob_visit_proffesor = prob_visit_proffesor
        self.notas_act = dict()
        self.notas_examen = dict()
        self.notas_controles = dict()
        self.notas_tareas = dict()
        self.initial_programmation_lvl = randrange(2, 11)
        self.catedra_help_days = []
        self.tips_days = []
        self.ayudantia_tips_days = []
        self.party_days = []
        self.meeting_days = []
        self.football_days = []
        self.active = True
        self.confidence = randrange(2, 13)
        self.id = next(Student.get_id)
        self.initial_confidence = self.confidence

    def id_():
        i = 0
        while True:
            yield i
            i += 1

    get_id = id_()

    @property
    def promedio(self):
        '''Returns the average score to the current date '''
        act_avg = sum(v for k, v in self.notas_act.items()) / len(self.notas_act) if len(self.notas_act) != 0 else None
        examen_avg = list(self.notas_examen.values()).pop() if len(self.notas_examen) != 0 else None
        controles_avg = sum(v for k, v in self.notas_controles.items()) / len(self.notas_controles) if len(self.notas_controles) != 0 else None
        tareas_avg = sum(v for k, v in self.notas_tareas.items()) / len(self.notas_tareas) if len(self.notas_tareas) != 0 else None

        Sum = 0
        n = 0
        if act_avg:
            Sum += act_avg
            n += 1
        if examen_avg:
            Sum += examen_avg
            n += 1
        if controles_avg:
            Sum += controles_avg
            n += 1
        if tareas_avg:
            Sum += tareas_avg
            n += 1

        return Sum / n if n != 0 else 1.0

    @property
    def tips_weeks(self):
        '''returns a list with the dates but in weeks '''
        return [int(tips_day / 7) for tips_day in self.tips_days]

    @property
    def party_weeks(self):
        return [int(party_day / 7) for party_day in self.party_days]

    @property
    def catedra_help_weeks(self):
        return [int(day / 7) for day in self.catedra_help_days]

    @property
    def ayudantia_tips_weeks(self):
        return [int(day / 7) for day in self.ayudantia_tips_days]

    @property
    def hangover_days(self):
        '''returns a list with days with hangover, ie, 2 days after party '''
        hang = []
        for day in self.party_days:
            hang.append(day + 1)
            hang.append(day + 2)
        return hang

    @property
    def meeting_weeks(self):
        return [int(meeting_day / 7) for meeting_day in self.meeting_days]

    def update_programming_level(self, time_day):
        '''This gets updated every catedra '''
        time_week = int(time_day / 7)
        v = 0.08 if time_week in self.meeting_weeks else 0
        w = 0.015 if time_week in self.party_weeks else 0
        previous = self.initial_programmation_lvl if time_week == 0 else self.programming_levels_dict[time_week - 1]
        self.programming_levels_dict[time_week] = 1.05 * (1 - + w - v) * previous

    def listen_tip(self, time_day):
        '''Add the day when the student listened a tip to a list '''
        self.tips_days.append(time_day)

    def visit_proffesor(self, time_day, proffesor):
        '''Adds the day when the student went to visit the teacher to a list '''
        if self.promedio <= 5.0:
            proffesor.cola.append(self)
        else:
            if bool(bernoulli(0.2)):
                proffesor.cola.append(self)

    def go_to_party(self, time_day):
        self.party_days.append(time_day)

    def update_confidence(self, time_day, n_a=False, n_t=False, n_c=False):
        '''Every time an evaluation is submitted, this gets updated. Updates the confindence'''
        x = 1 if n_a else 0
        y = 1 if n_t else 0
        z = 1 if n_c else 0
        scores_confidence = 0

        if bool(x):
            n_a_esperada = self.get_nota_esperada(time_day - 14)
            scores_confidence += 3 * (n_a - n_a_esperada)
        if bool(y):
            n_t_esperada = self.get_nota_esperada(time_day - 14)
            scores_confidence += 5 * (n_t - n_t_esperada)
        if bool(z):
            n_c_esperada = self.get_nota_esperada(time_day - 14)
            scores_confidence += 1 * (n_c - n_c_esperada)

        self.confidence += scores_confidence

    def get_nota_esperada(self, time_day):
        '''Returns the spected score acording to the table '''
        horas_estudiadas = int(self.get_horas_estudiadas(time_day))
        for rango_notas, horas in Student.nota_esperada.items():
            if horas[int(time_day / 7)][0] <= horas_estudiadas <= horas[int(time_day / 7)][1]:
                return round(uniform(rango_notas[0], rango_notas[1]), 2)

    def get_horas_estudiadas(self, time_day):
        '''Calculates and returns the amount of hours, depending on the events. '''
        self.horas_estudiadas = {i: 0 for i in range(0, 12)}
        for i in range(time_day):
            time_week = int(i / 7)
            horas_por_dia = 0.3 * self.horas_totales_semanas[time_week] / 7
            if i not in self.hangover_days and i not in self.football_days:
                self.horas_estudiadas[time_week] += horas_por_dia

        return self.horas_estudiadas[int(time_day / 7)]

    def get_horas_tareas(self, time_day, publication_date):
        '''Calculates and returns the amount of hours dedicated to a tarea. '''
        horas = 0
        for i in range(publication_date, time_day):
            time_week = int(i / 7)
            horas_por_dia = 0.7 * self.horas_totales_semanas[time_week] / 7
            if i not in self.hangover_days and i not in self.football_days:
                horas += horas_por_dia
        return horas

    def watch_football(self, time_day):
        '''Adds the date to a list, so it can be used to update other atributes '''
        self.football_days.append(time_day)

    def get_manejo_contenidos(self, time_day):
        '''Calculates and returns the contents skills. It returns the contents skills of the last week. '''
        self.get_horas_estudiadas(time_day)
        for i in range(time_day):
            time_week = int(time_day / 7)
            x = 1.0
            if time_week in self.tips_weeks:
                x *= 1.1
            if time_week in self.ayudantia_tips_weeks:
                x *= 1.1
            if time_week in self.catedra_help_weeks:
                n = self.catedra_help_weeks.count(time_week)
                x *= 1.0 + 0.01 * n
            self.manejo_contenidos[time_week] = (self.horas_estudiadas[time_week] / Student.dificulty[time_week]) * x

        return self.manejo_contenidos[int(time_day / 7)]

    def rendir_evaluacion(self, time_day, eval_name, exigencia, publication_date=False):
        '''It calculate the grade in every evaluation. It does not support exams '''
        time_week = int(time_day / 7)
        if eval_name == 'actividad':
            pep_8 = 0.7 * self.get_manejo_contenidos(time_day) + \
                0.2 * self.programming_levels_dict[time_week] + \
                0.1 * self.confidence
            functionality = 0.3 * self.get_manejo_contenidos(time_day) + \
                0.7 * self.programming_levels_dict[time_week] + \
                0.1 * self.confidence
            contents = 0.7 * self.get_manejo_contenidos(time_day) + \
                0.2 * self.programming_levels_dict[time_week] + \
                0.1 * self.confidence
            total = 0.4 * functionality + 0.4 * contents + 0.2 * pep_8
            nota = max(total * 7 / exigencia, 1)
            if self.personality == 'efficient':
                if time_week == 4 or time_week == 7:
                    nota = min(nota + 1, 7)
            elif self.personality == 'artistic':
                if time_week == 8 or time_week == 11:
                    nota = min(nota + 1, 7)
            elif self.personality == 'theoretical':
                if time_week == 5:
                    nota = min(nota + 1, 7)
            return nota
        elif eval_name == 'control':
            functionality = 0.3 * self.get_manejo_contenidos(time_day) + \
                0.2 * self.programming_levels_dict[time_week] + \
                0.5 * self.confidence
            contents = 0.7 * self.get_manejo_contenidos(time_day) + \
                0.05 * self.programming_levels_dict[time_week] + \
                0.25 * self.confidence
            total = 0.3 * functionality + 0.7 * contents
            nota = max(total * 7 / exigencia, 1)
            return nota
        elif eval_name == 'tarea':
            pep_8 = 0.5 * self.get_horas_tareas(time_day, publication_date) + 0.5 * self.programming_levels_dict[time_week]
            contents = 0.7 * self.get_manejo_contenidos(time_day) + 0.1 * self.programming_levels_dict[time_week] + 0.2 * self.get_horas_tareas(time_day, publication_date)
            functionality = 0.5 * self.get_manejo_contenidos(time_day) + 0.1 * self.programming_levels_dict[time_week] + 0.4 * self.get_horas_tareas(time_day, publication_date)
            if self.personality == 'efficient':
                pep_8 *= 1.1
                contents *= 1.1
                functionality *= 1.1
            elif self.personality == 'artistic':
                pep_8 *= 1.2
            elif self.personality == 'theoretical':
                pep_8 *= 0.9
                contents *= 0.9
                functionality *= 0.9
            total = 0.4 * functionality + 0.4 * contents + 0.2 * pep_8
            nota = max(total * 7 / exigencia, 1)
            return nota

    def rendir_examen(self, time_day, materias, exigencias):
        '''Calculates the grade in the case of exam. Returns the value '''
        time_week = int(time_day / 7)
        notas_preguntas = []
        for materia, exigencia in zip(materias, exigencias):
            contents = 0.5 * self.manejo_contenidos[time_week] + 0.1 * self.programming_levels_dict[time_week] + 0.4 * self.confidence
            functionality = 0.3 * self.manejo_contenidos[time_week] + 0.2 * self.programming_levels_dict[time_week] + 0.5 * self.confidence
            total_pregunta = 0.3 * functionality + 0.7 * contents
            nota_pregunta = max(total_pregunta * 7 / exigencia, 1)
            notas_preguntas.append(nota_pregunta)
        nota_final = sum(notas_preguntas) / len(notas_preguntas)
        if self.personality == 'theoretical':
            nota_final = min(nota_final + 1, 7)
        return nota_final

    def ask_questions(self, time_day, n_questions):
        '''Simulates the questions asked to an assistant. Adds to a list so it can be used to update other attributes '''
        for i in range(n_questions):
            self.catedra_help_days.append(time_day)

    def listen_ayudantia(self, time_day):
        '''Used when an assistant gives a super ayudantia. Adds date to a list '''
        self.ayudantia_tips_days.append(time_day)


class Simulation:
    '''Class to control all the instances of AdvancedProgramming. It can show the final statistics '''
    def __init__(self, prob_40_credits, prob_50_credits, prob_55_credits, prob_60_credits,
                 prob_visit_proffesor, prob_atraso_mavrakis, percentaje_progress_tarea_mail, month_party,
                 month_football, initial_level_confidence_inf, initial_level_confidence_sup):
        self.prob_40_credits = prob_40_credits
        self.prob_50_credits = prob_50_credits
        self.prob_55_credits = prob_55_credits
        self.prob_60_credits = prob_60_credits
        self.prob_visit_proffesor = prob_visit_proffesor
        self.prob_atraso_mavrakis = prob_atraso_mavrakis
        self.percentaje_progress_tarea_mail = percentaje_progress_tarea_mail
        self.month_football = month_football
        self.month_party = month_party
        self.initial_level_confidence_inf = initial_level_confidence_inf
        self.initial_level_confidence_sup = initial_level_confidence_sup
        self.escenarios_filename = 'escenarios.csv'

    def load(self):
        '''Loads all the csv files '''
        self.IIC = AdvancedProgramming(self.percentaje_progress_tarea_mail, self.month_party, self.month_football)
        with open('integrantes.csv', 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f, delimiter=',')
            header = next(csv_reader)
            for row in csv_reader:
                name = row[0]
                rol = row[1]
                section_number = row[2]
                if rol == 'Profesor':
                    person = Proffessor(name)
                elif rol == 'Coordinación':
                    person = Coordinator(name)
                elif rol == 'Docencia':
                    person = TeacherAssistant(name)
                elif rol == 'Tareas':
                    person = TaskAssistant(name)
                elif rol == 'Alumno':
                    person = Student(name, self.prob_40_credits, self.prob_50_credits,
                                     self.prob_55_credits, self.prob_60_credits, self.prob_visit_proffesor,
                                     self.initial_level_confidence_inf, self.initial_level_confidence_sup)

                self.IIC.add_person(person, section_number)

    def get_global_statistics(self):
        botaron = len(self.IIC.all_students) - len(self.IIC.active_students)
        avg_confidence = (sum([alumno.initial_confidence for alumno in self.IIC.all_students]) / len(self.IIC.all_students) +\
                          sum([alumno.confidence for alumno in self.IIC.active_students]) / len(self.IIC.active_students)) / 2
        print('[1] Cantidad total de alumnos que botaron el ramo: {}'.format(botaron))
        print('[2] Promedio de confianza al inicio y al final del ramo: {}'.format(avg_confidence))

    def get_personal_statistics(self):
        loop = True
        while loop:
            user_name = input('Ingrese el nombre completo del alumno').title()
            try:
                alumno = [i for i in self.IIC.all_students if i.name == user_name].pop()
            except IndexError:
                loop = True
            else:
                loop = False
        avg_prog_lvl = sum([v for k, v in alumno.programming_levels_dict.items()]) / len(alumno.programming_levels_dict)
        print('Nivel programacion promedio: '.format(avg_prog_lvl))
        print('Confianza final: '.format(alumno.confidence))
        x = [i for i in range(12)]
        y = [v for k, v in alumno.manejo_contenidos.items()]
        plt.plot(x, y)
        plt.title('Manejo contenidos vs semanas')
        plt.xlabel('Semanas')
        plt.ylabel('Manejo contenidos')
        plt.show()
        print('Notas actividades: ')
        for k, v in alumno.notas_act.items():
            print(k, v)
        print('Notas tareas: ')
        for k, v in alumno.notas_tareas.items():
            print(k, v)
        print('Notas controles: ')
        for k, v in alumno.notas_controles.items():
            print(k, v)
        print('Nota examen: ')
        for k, v in alumno.notas_examen.items():
            print(k, v)

    def get_graphs(self):
        x = self.IIC.dataframe_proms['MATERIA']
        y_1 = self.IIC.dataframe_proms['PROM CONTROLES']
        y_2 = self.IIC.dataframe_proms['PROM TAREAS']
        y_3 = self.IIC.dataframe_proms['PROM ACT']

        plt.plot(x, y_1, label='PROM CONTROLES')
        plt.plot(x, y_2, label='PROM TAREAS')
        plt.plot(x, y_3, label='PROM ACT')



print("""*******************************************************
***                                                 ***
***         Bienvenido a Avanzacion Programada      ***
***                                                 ***
*******************************************************""")
print("------------------------------------------------------")

print("Bienvenido a Avanzacion Programada, aca podras simular el curso \n\
    de la dimension de Mavrakis")

s = Simulation(0.1, 0.7, 0.15, 0.05, 0.2, 0.1, 0.5, 1 / 30, 1 / 70, 2, 12)
s.load()
curso = s.IIC
