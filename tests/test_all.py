import unittest
from msl import scheduler as sch  # , scheduler.Time, scheduler.TimePeriod
# from msl.scheduler import Time
# from msl.scheduler import TimePeriod
# from msl.scheduler import Booking
# from msl.scheduler import IncorrectTimePeriodError


class TestScheduler(unittest.TestCase):
    def setUp(self) -> None:
        valid_config = { "valid interval": 15,
                         "rooms" : {"C-Cave": 3,
                                    "D-Tower": 7,
                                    "G-Mansion":20},
                         "buffer" : [["09:00","09:15"],
                                     ["13:15","13:45"],
                                     ["18:45","19:00"]],
                         "meetings":[]
                         }
        self.app = sch.getInstanceFromJSON(valid_config)

    def tearDown(self) -> None:
        self.app = None

    def test_pass(self):
        # TODO
        pass

    def test_time_object_creation_valid(self):
        self.assertTrue(str(sch.Time("00:45")))
        self.assertIsInstance(sch.Time("00:15"), sch.Time)
        self.assertEqual("00:45", str(sch.Time("-00:45")))
        self.assertEqual("00:00", str(sch.Time("00:-00")))
        self.assertEqual(sch.Time("23:00"), sch.Time("23:00"))
        # self.assertEqual(sch.Time("23:15"), sch.Time("23:15"))

    def test_time_comparison(self):
        self.assertGreater(sch.Time("00:45"), sch.Time("00:30"))
        self.assertEqual(sch.Time("00:45"), sch.Time("-00:45"))

    def test_time_str_invalid(self):
        # self.assertRaises(ValueError, lambda: sch.Time("24:00"))
        # self.assertRaises(ValueError, lambda: sch.Time("2400"))
        # self.assertRaises(ValueError, lambda: )
        with self.assertRaises(ValueError):
            sch.Time("-12:00")
            sch.Time("24:00")
            sch.Time("1200")
        # sch.Time("12:00","5")

    def test_time_granularity_of_fifteen_minutes(self):
        # self.assertEqual(self.app.VALID_INTERVAL , 15)
        with self.assertRaises(ValueError):
            sch.Time("23:05")

    def test_timeperiod_creation_valid(self):
        start_one = sch.Time("00:15")
        end_one = sch.Time("00:30")
        self.assertTrue(sch.TimePeriod(start_one, end_one))

    def test_timeperiod_end_must_be_after_start(self):
        start_one = sch.Time("00:15")
        end_one = sch.Time("00:30")
        with self.assertRaises(ValueError):
            sch.TimePeriod(end_one,start_one)
            sch.TimePeriod(start_one,start_one)


    def test_timeperiod_with_tuples(self):
        self.assertRaises(TypeError, lambda: sch.TimePeriod((40,2),(41,5)))

    def test_TimePeriod_str_dunder(self):
        start_one = sch.Time("00:15")
        end_one = sch.Time("00:30")
        self.assertEqual("00:15-00:30", sch.TimePeriod(start_one, end_one).__str__())

    def test_app_has_rooms(self):
        self.assertEqual("C-Cave: 3, D-Tower: 7, G-Mansion: 20", ", ".join(map(str,self.app.rooms)))

    def test_pass_vacancy(self):
        self.assertEqual("C-Cave D-Tower G-Mansion", self.app.vacancy("09:30","10:00"))

    def test_fail_vacancy(self):

        self.assertEqual("", self.app.vacancy("09:00","11:00"),"clashes with buffer")

    def test_book(self):
        no_of_people = 3
        self.assertEqual("C-Cave", self.app.book("10:00","11:00", no_of_people))
        self.assertEqual("D-Tower", self.app.book("10:00","11:00", no_of_people))
        self.assertEqual("G-Mansion", self.app.book("10:00","11:00", no_of_people))
        self.assertEqual("", self.app.book("10:00","11:00", no_of_people))
        self.assertEqual(3,len(self.app.meetings))
        self.assertEqual("", self.app.book("11:00","12:00", no_of_people))
        self.assertEqual(4,len(self.app.meetings))


if __name__ == '__main__':
    unittest.main()
