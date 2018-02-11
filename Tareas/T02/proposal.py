
class Proposal:
    def __init__(self, priority, message, origin):
        self.priority = round(float(priority), 4)
        self.message = str(message)
        self.origin = origin

    def __repr__(self):
        return "Proposal(" + str(self.priority) + ", " + str(self.message) + ")"

    def __lt__(self, other):
        return self.priority < other.priority


def main():
    from linked_lists import LinkedList, LinkedQueue

    prop_1 = Proposal(5, 'close airtports', 'chile')
    prop_2 = Proposal(3, 'open airtports', 'chile')
    prop_3 = Proposal(20, 'give masks', 'chile')
    prop_4 = Proposal(6, 'give masks', 'chile')

    linked_queue = LinkedQueue(prop_1, prop_2, prop_3)
    print(linked_queue)
    linked_queue.sort_append(prop_4)
    print(linked_queue)


if __name__ == "__main__":
    main()
