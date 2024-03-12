#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dynamic Weather parameters class defintions. 

This code was inspired by one of the carla GitHub (https://github.com/carla-simulator/carla/blob/master/PythonAPI/examples/dynamic_weather.py).
"""

import math


class Sun(object):
    """The sun, which changes position smoothly with time"""

    def __init__(self, t):
        """Sets the intitial position of the sun"""
        self.tick(t)

    def tick(self, t):
        """Updates the position of the sun"""
        self.azimuth = self._get_azimuth(t)
        self.altitude = self._get_altitude(t)

    def _get_azimuth(self, t):
        return t * 360/18000

    def _get_altitude(self, t):
        x = 3/2 * math.pi + t * 2 * math.pi / 18000
        x %= 2.0 * math.pi
        return 30 * math.sin(x) + 15



class Weather(object):
    """The Weather, which changes dynamically over time"""

    def __init__(self, weather, t):
        self.weather = weather
        self.sun = Sun(t)
        self._update_weather_parameters(t)
        # We set the value of the parameters which will not change value over time
        self.weather.fog_distance = 0.75
        self.weather.fog_falloff = 0.1
        self.weather.wetness = 0.0
        self.weather.scattering_intensity = 1.0
        self.weather.mie_scattering_scale = 0.03
        self.weather.rayleigh_scattering_scale = 0.0331

    def tick(self, t):
        self.sun.tick(t)
        self._update_weather_parameters(t)

    def _update_weather_parameters(self, t):
        # We update the sun position
        self.weather.sun_azimuth_angle = self.sun.azimuth
        self.weather.sun_altitude_angle = self.sun.altitude

        # Values of the weather parameters for clear, rainy and foggy weathers
        CLOUDINESS_CLEAR = 5
        PRECIPITATION_CLEAR = 0
        PRECIPITATION_DEPOSIT_CLEAR = 0
        WIND_INTENSITY_CLEAR = 10
        FOG_DENSITY_CLEAR = 2

        CLOUDINESS_RAINY = 50
        PRECIPITATION_RAINY = 90
        PRECIPITATION_DEPOSIT_RAINY = 80
        WIND_INTENSITY_RAINY = 100
        FOG_DENSITY_RAINY = 7

        CLOUDINESS_FOGGY = 50
        PRECIPITATION_FOGGY = 0
        PRECIPITATION_DEPOSIT_FOGGY = 0
        WIND_INTENSITY_FOGGY = 10
        FOG_DENSITY_FOGGY = 70

        # We update the other weather parameters if needed
        if (t>=0 and t<=600) or (t>=3010 and t<=3600) or (t>=4210 and t<=4800) or (t>=5410 and t<=6000) or (t>=7810 and t<=8400) or (t>=9010 and t<=9600) or (t>=12010 and t<=12600) or (t>=13810 and t<=14400) or (t>=15010 and t<=15600) or (t>=16210 and t<=16800) :
            # clear weather
            self.weather.cloudiness = CLOUDINESS_CLEAR
            self.weather.precipitation = PRECIPITATION_CLEAR
            self.weather.precipitation_deposits = PRECIPITATION_DEPOSIT_CLEAR
            self.weather.wind_intensity = WIND_INTENSITY_CLEAR
            self.weather.fog_density = FOG_DENSITY_CLEAR

        elif (t>=610 and t<=1200) or (t>=1810 and t<=2400) or (t>=4810 and t<=5400) or (t>=6610 and t<=7200) or (t>=8410 and t<=9000) or (t>=10210 and t<=10800) or (t>=11410 and t<=12000) or (t>=12610 and t<=13200) or (t>=14410 and t<=15000) or (t>=17410 and t<=18000) :
            # rainy weather
            self.weather.cloudiness = CLOUDINESS_RAINY
            self.weather.precipitation = PRECIPITATION_RAINY
            self.weather.precipitation_deposits = PRECIPITATION_DEPOSIT_RAINY
            self.weather.wind_intensity = WIND_INTENSITY_RAINY
            self.weather.fog_density = FOG_DENSITY_RAINY

        elif (t>=1210 and t<=1800) or (t>=2410 and t<=3000) or (t>=3610 and t<=4200) or (t>=6010 and t<=6600) or (t>=7210 and t<=7800) or (t>=9610 and t<=10200) or (t>=10810 and t<=11400) or (t>=13210 and t<=13800) or (t>=15610 and t<=16200) or (t>=16810 and t<=17400) :
            # foggy weather
            self.weather.cloudiness = CLOUDINESS_FOGGY
            self.weather.precipitation = PRECIPITATION_FOGGY
            self.weather.precipitation_deposits = PRECIPITATION_DEPOSIT_FOGGY
            self.weather.wind_intensity = WIND_INTENSITY_FOGGY
            self.weather.fog_density = FOG_DENSITY_FOGGY

        elif (t>600 and t<610) or (t>4800 and t<4810) or (t>8400 and t<8410) or (t>12600 and t<12610) or (t>14400 and t<14410) :
            # transition from clear to rainy weather
            self.weather.cloudiness = CLOUDINESS_CLEAR + (CLOUDINESS_RAINY-CLOUDINESS_CLEAR)*(t%10)/10
            self.weather.precipitation = PRECIPITATION_CLEAR + (PRECIPITATION_RAINY-PRECIPITATION_CLEAR)*(t%10)/10
            self.weather.precipitation_deposits = PRECIPITATION_DEPOSIT_CLEAR + (PRECIPITATION_DEPOSIT_RAINY-PRECIPITATION_DEPOSIT_CLEAR)*(t%10)/10
            self.weather.wind_intensity = WIND_INTENSITY_CLEAR + (WIND_INTENSITY_RAINY-WIND_INTENSITY_CLEAR)*(t%10)/10
            self.weather.fog_density =  FOG_DENSITY_CLEAR + (FOG_DENSITY_RAINY-FOG_DENSITY_CLEAR)*(t%10)/10

        elif (t>3600 and t<3610) or (t>6000 and t<6010) or (t>9600 and t<9610) or (t>15600 and t<15610) or (t>16800 and t<16810) :
            # transition from clear to foggy weather
            self.weather.cloudiness = CLOUDINESS_CLEAR + (CLOUDINESS_FOGGY-CLOUDINESS_CLEAR)*(t%10)/10
            self.weather.precipitation = PRECIPITATION_CLEAR + (PRECIPITATION_FOGGY-PRECIPITATION_CLEAR)*(t%10)/10
            self.weather.precipitation_deposits = PRECIPITATION_DEPOSIT_CLEAR + (PRECIPITATION_DEPOSIT_FOGGY-PRECIPITATION_DEPOSIT_CLEAR)*(t%10)/10
            self.weather.wind_intensity = WIND_INTENSITY_CLEAR + (WIND_INTENSITY_FOGGY-WIND_INTENSITY_CLEAR)*(t%10)/10
            self.weather.fog_density =  FOG_DENSITY_CLEAR + (FOG_DENSITY_FOGGY-FOG_DENSITY_CLEAR)*(t%10)/10

        elif (t>5400 and t<5410) or (t>9000 and t<9010) or (t>12000 and t<12010) or (t>15000 and t<15010) :
            # transition from rainy to clear weather
            self.weather.cloudiness = CLOUDINESS_RAINY + (CLOUDINESS_CLEAR-CLOUDINESS_RAINY)*(t%10)/10
            self.weather.precipitation = PRECIPITATION_RAINY + (PRECIPITATION_CLEAR-PRECIPITATION_RAINY)*(t%10)/10
            self.weather.precipitation_deposits = PRECIPITATION_DEPOSIT_RAINY + (PRECIPITATION_DEPOSIT_CLEAR-PRECIPITATION_DEPOSIT_RAINY)*(t%10)/10
            self.weather.wind_intensity = WIND_INTENSITY_RAINY + (WIND_INTENSITY_CLEAR-WIND_INTENSITY_RAINY)*(t%10)/10
            self.weather.fog_density =  FOG_DENSITY_RAINY + (FOG_DENSITY_CLEAR-FOG_DENSITY_RAINY)*(t%10)/10

        elif (t>1200 and t<1210) or (t>2400 and t<2410) or (t>7200 and t<7210) or (t>10800 and t<10810) or (t>13200 and t<13210) :
            # transition from rainy to foggy weather
            self.weather.cloudiness = CLOUDINESS_RAINY + (CLOUDINESS_FOGGY-CLOUDINESS_RAINY)*(t%10)/10
            self.weather.precipitation = PRECIPITATION_RAINY + (PRECIPITATION_FOGGY-PRECIPITATION_RAINY)*(t%10)/10
            self.weather.precipitation_deposits = PRECIPITATION_DEPOSIT_RAINY + (PRECIPITATION_DEPOSIT_FOGGY-PRECIPITATION_DEPOSIT_RAINY)*(t%10)/10
            self.weather.wind_intensity = WIND_INTENSITY_RAINY + (WIND_INTENSITY_FOGGY-WIND_INTENSITY_RAINY)*(t%10)/10
            self.weather.fog_density =  FOG_DENSITY_RAINY + (FOG_DENSITY_FOGGY-FOG_DENSITY_RAINY)*(t%10)/10

        elif (t>3000 and t<3010) or (t>4200 and t<4210) or (t>7800 and t<7810) or (t>13800 and t<13810) or (t>16200 and t<16210) :
            # transition from foggy to clear weather
            self.weather.cloudiness = CLOUDINESS_FOGGY + (CLOUDINESS_CLEAR-CLOUDINESS_FOGGY)*(t%10)/10
            self.weather.precipitation = PRECIPITATION_FOGGY + (PRECIPITATION_CLEAR-PRECIPITATION_FOGGY)*(t%10)/10
            self.weather.precipitation_deposits = PRECIPITATION_DEPOSIT_FOGGY + (PRECIPITATION_DEPOSIT_CLEAR-PRECIPITATION_DEPOSIT_FOGGY)*(t%10)/10
            self.weather.wind_intensity = WIND_INTENSITY_FOGGY + (WIND_INTENSITY_CLEAR-WIND_INTENSITY_FOGGY)*(t%10)/10
            self.weather.fog_density =  FOG_DENSITY_FOGGY + (FOG_DENSITY_CLEAR- FOG_DENSITY_FOGGY)*(t%10)/10

        elif (t>1800 and t<1810) or (t>6600 and t<6610) or (t>10200 and t<10210) or (t>11400 and t<11410) or (t>17400 and t<17410) :
            # transition from foggy to rainy weather
            self.weather.cloudiness = CLOUDINESS_FOGGY + (CLOUDINESS_RAINY-CLOUDINESS_FOGGY)*(t%10)/10
            self.weather.precipitation = PRECIPITATION_FOGGY + (PRECIPITATION_RAINY-PRECIPITATION_FOGGY)*(t%10)/10
            self.weather.precipitation_deposits = PRECIPITATION_DEPOSIT_FOGGY + (PRECIPITATION_DEPOSIT_RAINY-PRECIPITATION_DEPOSIT_FOGGY)*(t%10)/10
            self.weather.wind_intensity = WIND_INTENSITY_FOGGY + (WIND_INTENSITY_RAINY-WIND_INTENSITY_FOGGY)*(t%10)/10
            self.weather.fog_density =  FOG_DENSITY_FOGGY + (FOG_DENSITY_RAINY- FOG_DENSITY_FOGGY)*(t%10)/10
