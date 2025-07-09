import unittest
from turbo_rally import Vehicle, Track, Weather, Race


class RaceTests(unittest.TestCase):
    def test_race_records_time(self):
        vehicle = Vehicle('Test Car', 140, 0.9, 0.8)
        track = Track('Test Track', 'gravel', 1.0, [])
        weather = Weather('clear')
        race = Race(track, weather, laps=1)
        times = race.run(vehicle)
        self.assertEqual(len(times), 1)
        self.assertGreater(times[0], 0)
        self.assertIn('Test Car', race.leaderboard)


if __name__ == '__main__':
    unittest.main()

