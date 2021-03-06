import pandas as pd
from mamba import description, context, it
from expects import expect, equal
from blsqpy.periods import Periods
from datetime import date

with description("dhis2 split") as self:

    with it("converts month to quarter"):
        expect(Periods.split("201601", "quarterly")).to(equal(("2016Q1",)))
        expect(Periods.split("201602", "quarterly")).to(equal(("2016Q1",)))
        expect(Periods.split("201603", "quarterly")).to(equal(("2016Q1",)))

    with it("converts month to year"):
        expect(Periods.split("201601", "yearly")).to(equal(
            ("2016",)))

    with it("converts quarter to months"):
        expect(Periods.split("2016Q1", "monthly")).to(equal(
            ("201601", "201602", "201603")))
        expect(Periods.split("2016Q2", "monthly")).to(
            equal(("201604", "201605", "201606")))
        expect(Periods.split("2016Q3", "monthly")).to(
            equal(("201607", "201608", "201609")))
        expect(Periods.split("2016Q4", "monthly")).to(
            equal(("201610", "201611", "201612")))

    with it("converts quarter to year"):
        expect(Periods.split("2016Q1", "yearly")).to(equal(
            ("2016",)))

    with it("converts year to quarter"):
        expect(Periods.split("2016", "quarterly")).to(equal(
            ("2016Q1", "2016Q2", "2016Q3", "2016Q4")))

    with it("converts year to months"):
        expect(Periods.split("2016", "monthly")).to(equal(
            ('201601', '201602', '201603', '201604', '201605', '201606', '201607',
             '201608', '201609', '201610', '201611', '201612')))

    with it("converts financial year july to year"):
        expect(Periods.split("2015July", "yearly")).to(equal(
            ("2015", "2016")))
        expect(Periods.split("2016July", "yearly")).to(equal(
            ("2016", "2017")))

    with it("converts month to financial year july"):
        expect(Periods.split("201601", "financial_july")).to(equal(
            ("2015July",)))
        expect(Periods.split("201606", "financial_july")).to(equal(
            ("2015July",)))
        expect(Periods.split("201607", "financial_july")).to(equal(
            ("2016July",)))
        expect(Periods.split("201701", "financial_july")).to(equal(
            ("2016July",)))

    with it("converts quarter to financial year july"):
        expect(Periods.split("2016Q1", "financial_july")).to(equal(
            ("2015July",)))
        expect(Periods.split("2016Q2", "financial_july")).to(equal(
            ("2015July",)))
        expect(Periods.split("2016Q3", "financial_july")).to(equal(
            ("2016July",)))
        expect(Periods.split("2016Q4", "financial_july")).to(equal(
            ("2016July",)))
        expect(Periods.split("2017Q1", "financial_july")).to(equal(
            ("2016July",)))
        expect(Periods.split("2017Q2", "financial_july")).to(equal(
            ("2016July",)))

    with it("cached and non cached version returns same type"):
        first = Periods.split("2018", "monthly")
        last = Periods.split("2018", "monthly")
        expect(first).to(equal(last))

with description("as_date_range") as self:

    with it("correct range for monthly"):
        expect(Periods.as_date_range("201601").start).to(
            equal(date(2016, 1, 1)))
        expect(Periods.as_date_range("201601").end).to(
            equal(date(2016, 1, 31)))

    with it("correct range for quarter"):
        expect(Periods.as_date_range("2016Q3").start).to(
            equal(date(2016, 7, 1)))
        expect(Periods.as_date_range("2016Q3").end).to(
            equal(date(2016, 9, 30)))
        expect(Periods.as_date_range("2016Q4").start).to(
            equal(date(2016, 10, 1)))
        expect(Periods.as_date_range("2016Q4").end).to(
            equal(date(2016, 12, 31)))

    with it("correct range for year"):
        expect(Periods.as_date_range("2016").start).to(equal(date(2016, 1, 1)))
        expect(Periods.as_date_range("2016").end).to(equal(date(2016, 12, 31)))

    with it("correct range for financial july year"):
        expect(Periods.as_date_range("2016July").start).to(
            equal(date(2016, 7, 1)))
        expect(Periods.as_date_range("2016July").end).to(
            equal(date(2017, 6, 30)))
        expect(Periods.as_date_range("2017July").start).to(
            equal(date(2017, 7, 1)))
        expect(Periods.as_date_range("2017July").end).to(
            equal(date(2018, 6, 30)))

with description("add_period_columns") as self:
    with it("quarter and monthly columns"):
        df = pd.DataFrame(
            data=[
                ["2018-10-31", "monthly", "org1"],
                ["2018-10-31", "quarterly", "org2"]
            ],
            index=["0", "1"],
            columns=['start_date', 'frequency', "extra"])
        df['start_date'] = pd.to_datetime(df['start_date'], format='%Y-%m-%d')
        df = Periods.add_period_columns(df)
        print(df)

        expected_df = pd.DataFrame(
            data=[
                ["org1", "201810", "2018Q4"],
                ["org2", None, "2018Q4"]
            ],
            index=["0", "1"],
            columns=["extra", 'monthly', 'quarterly'])

        print(expected_df)
        pd.testing.assert_frame_equal(
            df,
            expected_df, check_dtype=False, check_index_type=False)
