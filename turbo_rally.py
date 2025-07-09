"""Turbo Rally - simplified rally racing simulation.

This module provides a minimal text-based implementation of the
Turbo Rally game. It demonstrates vehicle selection, weather and
terrain effects, a basic physics model and lap time tracking.
"""

from dataclasses import dataclass
import random
from typing import List, Dict


@dataclass
class Vehicle:
    name: str
    speed: float  # base top speed
    handling: float  # traction / handling rating
    acceleration: float  # acceleration rating

    def performance_modifier(self) -> float:
        """Combined modifier from handling and acceleration."""
        return (self.handling + self.acceleration) / 2


@dataclass
class Track:
    name: str
    terrain: str
    length_km: float
    obstacles: List[str]

    TERRAIN_EFFECT = {
        "mud": 0.7,
        "gravel": 0.85,
        "sand": 0.8,
    }

    def terrain_modifier(self) -> float:
        return self.TERRAIN_EFFECT.get(self.terrain, 1.0)


@dataclass
class Weather:
    condition: str  # e.g. clear, rain, storm

    WEATHER_EFFECT = {
        "clear": 1.0,
        "rain": 0.8,
        "storm": 0.7,
    }

    def traction_modifier(self) -> float:
        return self.WEATHER_EFFECT.get(self.condition, 1.0)


class Race:
    """Simulate a race on a track under certain weather."""

    def __init__(self, track: Track, weather: Weather, laps: int = 1):
        self.track = track
        self.weather = weather
        self.laps = laps
        self.leaderboard: Dict[str, float] = {}

    def _lap_time(self, vehicle: Vehicle) -> float:
        """Calculate lap time using a simple physics approximation."""
        base_speed = vehicle.speed * vehicle.performance_modifier()
        speed = base_speed * self.track.terrain_modifier() * self.weather.traction_modifier()
        # Add random penalty for obstacles to simulate collisions
        obstacle_penalty = len(self.track.obstacles) * random.uniform(0.5, 1.5)
        time_hours = self.track.length_km / max(speed - obstacle_penalty, 1)
        return time_hours * 60  # return minutes

    def run(self, vehicle: Vehicle) -> List[float]:
        times = []
        for lap in range(1, self.laps + 1):
            lap_time = self._lap_time(vehicle)
            times.append(lap_time)
            print(f"Lap {lap}: {lap_time:.2f} minutes")
        total_time = sum(times)
        print(f"Total race time: {total_time:.2f} minutes\n")
        self.leaderboard[vehicle.name] = total_time
        return times


# Default game data ---------------------------------------------------------

def default_vehicles() -> List[Vehicle]:
    return [
        Vehicle("Dust Rider", speed=140, handling=0.9, acceleration=0.8),
        Vehicle("Mud Crusher", speed=130, handling=0.95, acceleration=0.85),
        Vehicle("Gravel Master", speed=150, handling=0.85, acceleration=0.9),
        Vehicle("Sand Storm", speed=145, handling=0.8, acceleration=0.88),
        Vehicle("Rock Hopper", speed=135, handling=0.92, acceleration=0.83),
    ]


def default_tracks() -> List[Track]:
    return [
        Track(
            name="Forest Trail",
            terrain="mud",
            length_km=5.0,
            obstacles=["log", "puddle", "rock"],
        ),
        Track(
            name="Gravel Pass",
            terrain="gravel",
            length_km=4.5,
            obstacles=["rock", "ditch"],
        ),
        Track(
            name="Desert Run",
            terrain="sand",
            length_km=6.0,
            obstacles=["dune", "rock", "cactus"],
        ),
    ]


def choose_vehicle(vehicles: List[Vehicle]) -> Vehicle:
    print("Select your vehicle:")
    for idx, v in enumerate(vehicles, start=1):
        print(f" {idx}. {v.name} (Speed:{v.speed}, Handling:{v.handling}, Acc:{v.acceleration})")
    choice = int(input("Enter number: "))
    return vehicles[choice - 1]


def choose_track(tracks: List[Track]) -> Track:
    print("Select a track:")
    for idx, t in enumerate(tracks, start=1):
        print(f" {idx}. {t.name} - terrain: {t.terrain}, length: {t.length_km}km")
    choice = int(input("Enter number: "))
    return tracks[choice - 1]


def choose_weather() -> Weather:
    conditions = ["clear", "rain", "storm"]
    print("Select weather condition:")
    for idx, c in enumerate(conditions, start=1):
        print(f" {idx}. {c}")
    choice = int(input("Enter number: "))
    return Weather(conditions[choice - 1])


def main():
    vehicles = default_vehicles()
    tracks = default_tracks()
    vehicle = choose_vehicle(vehicles)
    track = choose_track(tracks)
    weather = choose_weather()
    laps = int(input("Number of laps: "))

    race = Race(track, weather, laps=laps)
    race.run(vehicle)

    print("Leaderboard:")
    for name, total in sorted(race.leaderboard.items(), key=lambda x: x[1]):
        print(f" {name}: {total:.2f} minutes")


if __name__ == "__main__":
    main()

