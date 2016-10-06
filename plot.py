import arrow
import numpy as np
import pandas as pd
import pygal


def plot_duration(df, filename):
    chart = pygal.Box(title='Commute duration', y_title='Minutes', show_legend=False, width=600, height=400)
    chart.x_labels = ['Home to work', 'Work to home']
    chart.add('Home to work', df['duration_s'][df['label'] == 'work'].values / 60)
    chart.add('Work to home', df['duration_s'][df['label'] == 'home'].values / 60)
    chart.render_to_png(filename)


def plot_duration_by_trip_start_time(df, label, filename):
    dff = df[df['label'] == label]

    x = map(lambda st: arrow.get(st).to('PST').time(), dff['started_at'].values)
    y = dff['duration_s'].values / 60

    chart = pygal.TimeLine(x_value_formatter=lambda dt: dt.strftime('%H:%M'), stroke=False, range=(0, max(y) + 15), width=600, height=400, x_title='Departure time',
                           y_title='Trip time (minutes)', title='Commute time by start time')

    chart.add(label, zip(x, y))
    chart.render_to_png(filename)


def plot_duration_by_day_of_week(df, label, filename):
    dff = df[df['label'] == label]

    durations_by_day_of_week = {}
    for t in dff[['started_at', 'duration_s']].values:
        day_of_week = arrow.get(t[0]).weekday()
        if day_of_week not in durations_by_day_of_week.keys():
            durations_by_day_of_week[day_of_week] = []

        durations_by_day_of_week[day_of_week].append(t[1] / 60)

    chart = pygal.Box(title='Commute to %s duration, by day of week' % (label), y_title='min', show_legend=False, width=600, height=400)
    l = arrow.locales.EnglishLocale()
    chart.x_labels = map(lambda d: l.day_name(d + 1), durations_by_day_of_week.keys())
    for (day_of_week, durations) in durations_by_day_of_week.iteritems():
        chart.add('To %s' % (label), durations)

    chart.render_to_png(filename)


def run(trips_filename):
    df = pd.read_csv(trips_filename, delimiter=',', names=['id', 'started_at', 'ended_at', 'duration_s', 'label'])
    # exclude outliers outside of 2 stddev
    df = df[np.abs(df.duration_s - df.duration_s.mean()) <= (2 * df.duration_s.std())]

    plot_duration(df, 'commute.png')
    plot_duration_by_trip_start_time(df, label='work', filename='commute_to_work_by_start.png')
    plot_duration_by_trip_start_time(df, label='home', filename='commute_to_home_by_start.png')
    plot_duration_by_day_of_week(df, label='work', filename='commute_to_work_by_day.png')
    plot_duration_by_day_of_week(df, label='home', filename='commute_to_home_by_day.png')


if __name__ == '__main__':
    run('out.csv')
