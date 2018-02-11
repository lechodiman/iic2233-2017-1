def intersect(x_0, y_0, r_0, x_1, y_1, r_1):

	return (r_0 - r_1)**2 <= (x_0 - x_1)**2 + (y_0 - y_1)**2 and \
			(x_0 - x_1)**2 + (y_0 - y_1)**2 >= (r_0 + r_1)**2


def is_bisiesto(year):

	leap = None
	if not year % 4 == 0:
		leap = False
	elif not year % 100 == 0:
		leap = True
	elif not year % 400:
		leap = False
	else:
		leap = True

	return leap

def grados_a_puntos(lat, lon):

	x = lat*110
	y = lon*110

	return (x,y)

#retorna distnacia en km entre dos puntos como (lat,lon)
def dist_entre_grados(tuple1, tuple2):
	
	lat1 = tuple1[0]
	lon1 = tuple1[1]

	lat2 = tuple2[0]
	lon2 = tuple2[1]

	p1 = grados_a_puntos(lat1, lon1)
	p2 = grados_a_puntos(lat2, lon2)

	dist = sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

	return dist