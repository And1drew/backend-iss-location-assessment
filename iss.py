#!/usr/bin/env python3

import sys
import turtle
import time
import requests

if sys.version_info[0] < 3:
    raise RuntimeError("Whoa there! we need py 3 to run this script")

__author__ = "Andrew Belanger(with demo)"

base_url ="http://api.open-notify.org"
iss_icon = 'iss.gif'
world_map = 'map.gif'


def get_astronauts():
    """Return a dict of astronauts and the spaceships """
    r = requests.get(base_url + '/astros.json')
    r.raise_for_status()
    return r.json()["people"]


def get_iss_location():
    """Returns the current location(lat, lon) of ISS as a float tuple"""
    r = requests.get(base_url + '/iss-now.json')
    r.raise_for_status()
    position = r.json()['iss_position']
    lat = float(position['latitude'])
    lon = float(position['longitude'])
    return lat, lon


def create_ISS():
    iss = turtle.Turtle()
    iss.shape(iss_icon)
    iss.setheading(90)
    lat, lon = get_iss_location()
    iss.penup()
    move_iss(iss, lon, lat)
    return iss


def move_iss(iss, lat, lon):
    iss.goto(lon, lat)


def update_iss_location():
    lat, lon = get_iss_location()
    move_iss(iss, lat, lon)
    turtle.ontimer(update_iss_location(), 1)


def create_map():
    """Draw a world map and make ISS turtle"""
    screen = turtle.Screen()
    screen.setup(720, 360)
    screen.bgpic(world_map)
    screen.setworldcoordinates(-180, -90, 180, 90)
    screen.register_shape(iss_icon)
    return screen


def compute_rise_time(lat, lon):
    """Return the next horizon rise-time of the ISS for a specific Coord"""
    params = {'lat': lat, 'lon': lon}
    r = requests.get(base_url + '/iss-pass.json', params=params)
    r.raise_for_status()
    passover_time = r.json()['response'][1]['risetime']
    return time.ctime(passover_time)


def create_indy():
    pos_lat = 39.768403
    pos_lon = -86.158068
    location = turtle.Turtle()
    location.penup()
    location.color('red')
    location.goto(pos_lon, pos_lat)
    location.dot(5)
    location.hideturtle()
    location.color('yellow')
    next_pass = compute_rise_time(pos_lat, pos_lon)
    location.write(next_pass, align='center')


def main():
    astro_dict = get_astronauts()
    print("\nCurrent number of people in space: {}".format(len(astro_dict)))
    for a in astro_dict:
        print(' - {} in {}'.format(a["name"], a["craft"]))

    lat, lon = get_iss_location()
    print('\nCurrent ISS Coords:  lat={:.02f} lon={:.02f}'.format(lat, lon))

    global iss
    screen = create_map()
    create_indy()
    iss = create_ISS()

    screen.ontimer(update_iss_location(), 5)


    if screen is not None:
        print("click screen to exit ...")
        screen.exitonclick()


if __name__ == '__main__':
    main()
