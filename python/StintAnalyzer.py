import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import time


class StintAnalyzer:


    def __init__(self, df1_path : str = None, df2_path : str = None, df1_name : str = 'Stint 1', df2_name : str = 'Stint 2', df1_skip_laps : list =[], df2_skip_laps : list=[]) -> None:
        
        if df1_path:
            self.df1 : pd.DataFrame = pd.read_csv(df1_path)
            self.df1_name : str = df1_name

        if df2_path:
            self.df2 : pd.DataFrame = pd.read_csv(df2_path)
            self.df2_name : str = df2_name
        else:
            if df1_path:
                self.df2 : pd.DataFrame = self.df1.copy(deep=True)
                self.df2_name : str = self.df1_name + '(Copy)'

        self.df1_skip_laps = df1_skip_laps
        self.df2_skip_laps = df2_skip_laps
        self.df1_fastest_lap : int
        self.df2_fastest_lap : int

        if df1_path:
            self.setup_stintanalyzer()
 

    def load_df1(self, buffer):
        self.df1=pd.read_csv(buffer)
        self.df1_name = 'Stint 1'


    def load_df2(self, buffer):
        self.df2=pd.read_csv(buffer)
        self.df2_name = 'Stint 2'
        
        self.setup_stintanalyzer()


    def setup_stintanalyzer(self):

        self._set_matplotlib_params()
        self._set_actual_lap_time()
        self.delete_laps_df1(self.df1_skip_laps)
        self.delete_laps_df2(self.df2_skip_laps)


    def _set_actual_lap_time(self):

        time_data_df1 = self.df1.groupby('Lap')['LapLastLapTime'].value_counts()
        time_dict_df1={}
        final_dict_df1={}
        for index in range(time_data_df1.index.get_level_values(0).min(), time_data_df1.index.get_level_values(0).max()+1):
            time_dict_df1[index] = time_data_df1[index].to_dict()
        for key in time_dict_df1.keys():
            final_dict_df1[key - 1] = max(time_dict_df1[key], key=time_dict_df1[key].get)
        # Delete in-/out-lap        
        self.df1.drop(self.df1[self.df1.Lap == self.df1.Lap.min()].index, inplace = True)
        self.df1.drop(self.df1[self.df1.Lap == self.df1.Lap.max()].index, inplace = True)
        self.df1['LapActualTime'] = self.df1['Lap'].apply(lambda lap: final_dict_df1[lap])
      
        time_data_df2 = self.df2.groupby('Lap')['LapLastLapTime'].value_counts()
        time_dict_df2={}
        final_dict_df2={}
        for index in range(time_data_df2.index.get_level_values(0).min(), time_data_df2.index.get_level_values(0).max()+1):
            time_dict_df2[index] = time_data_df2[index].to_dict()
        for key in time_dict_df2.keys():
            final_dict_df2[key - 1] = max(time_dict_df2[key], key=time_dict_df2[key].get)
        # Delete in-/out-lap        
        self.df2.drop(self.df2[self.df2.Lap == self.df2.Lap.min()].index, inplace = True)
        self.df2.drop(self.df2[self.df2.Lap == self.df2.Lap.max()].index, inplace = True)
        self.df2['LapActualTime'] = self.df2['Lap'].apply(lambda lap: final_dict_df2[lap])

        self.df1_fastest_lap = self.df1.groupby('Lap').LapActualTime.max().idxmin() 
        self.df2_fastest_lap = self.df2.groupby('Lap').LapActualTime.max().idxmin()


    def _set_matplotlib_params(self):
        plt.rcParams['font.family'] = ['Roboto', 'Arial', 'sans-serif']


    def _convert_in_min(self, seconds : float) -> str:
        value = int(seconds*1000%1000)
        if value == 0:
            ms = '000'
        elif value < 10:
            ms = '00' + str(value)
        elif value < 100:
            ms = '0' + str(value)
        else:
            ms = str(value)
        return time.strftime('%M:%S.{}'.format(ms), time.gmtime(seconds))


    def delete_laps_df1(self, laps : list) -> None:
        for lap in laps:
            self.df1.drop(self.df1[self.df1.Lap == int(lap)].index, inplace=True)


    def delete_laps_df2(self, laps: list) -> None:
        for lap in laps:
            self.df2.drop(self.df2[self.df2.Lap == int(lap)].index, inplace=True)


    def get_laps_overview(self, dataframe : str) -> pd.DataFrame:
        if dataframe == 'df1':
            data = self.df1.groupby('Lap').LapActualTime.max().to_frame()
        elif dataframe == 'df2':
            data = self.df2.groupby('Lap').LapActualTime.max().to_frame()
        data.columns=['Laptime']
        return data.Laptime.apply(self._convert_in_min).to_frame()


    def get_laptime_graph(self):
        
        lap_data_df1 = self.df1.groupby('Lap')['LapActualTime']
        lap_data_df2 = self.df2.groupby('Lap')['LapActualTime']

        fig, axes = plt.subplots(1, 2, sharey=True, figsize=(8,5))
        fig.suptitle('Lap Times', fontsize=14, fontweight=600)

        axes[0].set_title(self.df1_name, fontsize=10, fontweight=300)
        axes[1].set_title(self.df2_name, fontsize=10, fontweight=300)


        lap_data_df1.mean().plot(ax=axes[0], color='red', linewidth=2, drawstyle="steps-mid", label='laptime')
        axes[0].plot(lap_data_df1.max().index, [lap_data_df1.max().mean()] * len(lap_data_df1.max().index), label='mean')
        axes[0].plot(lap_data_df1.max().index, [lap_data_df1.max().median()] * len(lap_data_df1.max().index), label='median')

        lap_data_df2.mean().plot(ax=axes[1], color='red', linewidth=2, drawstyle="steps-mid", label='')
        axes[1].plot(lap_data_df2.max().index, [lap_data_df2.max().mean()] * len(lap_data_df2.max().index))
        axes[1].plot(lap_data_df2.max().index, [lap_data_df2.max().median()] * len(lap_data_df2.max().index))

        axes[0].set_ylabel('Laptime in sec.', fontsize=9)

        for axe in axes:
            for value in 'top right'.split():
                axe.spines[value].set_visible(False)
            axes[1].spines['left'].set_visible(False)
            axe.grid(axis='y', linestyle='--', linewidth=0.5)
            axe.tick_params(labelsize=9, length=0)
            axe.set_xlabel('Lap', fontsize=9)

        formatter = mpl.ticker.FuncFormatter(lambda s, x: time.strftime('%M:%S:{}'.format(int(s*100%100)), time.gmtime(s)))
        axes[0].yaxis.set_major_formatter(formatter)

        axes[0].legend(frameon = False)
        plt.tight_layout()
        return fig


    def get_speed_graph(self):

        fig, axes = plt.subplots(4, 2, figsize=(8,14), sharey='row')
        fig.suptitle('Speed Overview', fontsize=14, fontweight=600)

        df1_speed = self.df1.groupby(by='Lap').Speed
        df2_speed = self.df2.groupby(by='Lap').Speed

        axes[0, 0].set_title('Max. Speed ' + self.df1_name, fontsize=10, fontweight=300)
        axes[0, 1].set_title('Max Speed' + self.df2_name, fontsize=10, fontweight=300)
        df1_speed.max().plot(ax=axes[0, 0], drawstyle='steps-mid')
        df2_speed.max().plot(ax=axes[0, 1], drawstyle='steps-mid', label='')
        axes[0, 0].plot(df1_speed.max().index, [df1_speed.max().mean()] * len(df1_speed.max().index), label='mean')
        axes[0, 0].plot(df1_speed.max().index, [df1_speed.max().median()] * len(df1_speed.max().index), label='median')
        axes[0, 1].plot(df2_speed.max().index, [df2_speed.max().mean()] * len(df2_speed.max().index), label='')
        axes[0, 1].plot(df2_speed.max().index, [df2_speed.max().median()] * len(df2_speed.max().index), label='')
        axes[0, 0].legend(frameon = False)
        axes[0, 0].set_ylabel('Speed in km/h', fontsize=9)

        axes[1, 0].set_title('Avg. Speed ' + self.df1_name, fontsize=10, fontweight=300)
        axes[1, 1].set_title('Avg. Speed' + self.df2_name, fontsize=10, fontweight=300)
        df1_speed.mean().plot(ax=axes[1, 0], drawstyle='steps-mid')
        df2_speed.mean().plot(ax=axes[1, 1], drawstyle='steps-mid', label='')
        axes[1, 0].plot(df1_speed.mean().index, [df1_speed.mean().mean()] * len(df1_speed.mean().index), label='mean')
        axes[1, 0].plot(df1_speed.mean().index, [df1_speed.mean().median()] * len(df1_speed.mean().index), label='median')
        axes[1, 1].plot(df2_speed.mean().index, [df2_speed.mean().mean()] * len(df2_speed.mean().index), label='')
        axes[1, 1].plot(df2_speed.mean().index, [df2_speed.mean().median()] * len(df2_speed.mean().index), label='')
        axes[1, 0].legend(frameon = False)
        axes[1, 0].set_ylabel('Speed in km/h', fontsize=9)

        axes[2, 0].set_title('Min. Speed ' + self.df1_name, fontsize=10, fontweight=300)
        axes[2, 1].set_title('Min. Speed' + self.df2_name, fontsize=10, fontweight=300)
        df1_speed.min().plot(ax=axes[2, 0], drawstyle='steps-mid')
        df2_speed.min().plot(ax=axes[2, 1], drawstyle='steps-mid', label='')
        axes[2, 0].plot(df1_speed.min().index, [df1_speed.min().mean()] * len(df1_speed.min().index), label='mean')
        axes[2, 0].plot(df1_speed.min().index, [df1_speed.min().median()] * len(df1_speed.min().index), label='median')
        axes[2, 1].plot(df2_speed.min().index, [df2_speed.min().mean()] * len(df2_speed.min().index), label='')
        axes[2, 1].plot(df2_speed.min().index, [df2_speed.min().median()] * len(df2_speed.min().index), label='')
        axes[2, 0].legend(frameon = False)
        axes[2, 0].set_ylabel('Speed in km/h', fontsize=9)

        fastest_lap_df1 = self.df1.groupby('Lap').LapActualTime.max().idxmin()
        fastest_lap_df2 = self.df2.groupby('Lap').LapActualTime.max().idxmin()
        axes[3, 0].set_title(self.df1_name + ": Speed during fastest lap " + str(fastest_lap_df1), fontsize=12, fontweight=400)
        axes[3, 1].set_title(self.df2_name + ": Speed during fastest lap " + str(fastest_lap_df2), fontsize=12, fontweight=400)
        self.df1[self.df1.Lap == fastest_lap_df1].plot(ax=axes[3, 0], kind='scatter', x='Lat', y='Lon', s=50, c='Speed', cmap=mpl.colors.LinearSegmentedColormap.from_list("", ['maroon','brown', 'orange', 'yellow']))
        self.df2[self.df2.Lap == fastest_lap_df2].plot(ax=axes[3, 1], kind='scatter', x='Lat', y='Lon', s=50, c='Speed', cmap=mpl.colors.LinearSegmentedColormap.from_list("", ['maroon','brown', 'orange', 'yellow']))
        axes[3, 0].plot(self.df1.iloc[0]['Lat'], self.df1.iloc[0]['Lon'], "ro", label='start/finish line', ms=8)
        axes[3, 1].plot(self.df2.iloc[0]['Lat'], self.df2.iloc[0]['Lon'], "ro", label='start/finish line', ms=8)
        for axe in [axes[3, 0], axes[3, 1]]:
            for value in 'top right left bottom'.split():
                axe.spines[value].set_visible(False)
            axe.set_xlabel('')
            axe.set_ylabel('')
        axes[3, 0].tick_params(left = False, right = False, labelleft = False, labelbottom = False, bottom = False)
        axes[3, 1].tick_params(left = False, right = False, labelleft = False, labelbottom = False, bottom = False)
        axes[3, 0].legend(frameon=False)
        axes[3, 1].legend(frameon=False)

        plt.tight_layout()
        return fig


    def get_computer_performance_graph(self):
        fig, axes = plt.subplots(4, 2, figsize=(8,12), sharey='row')
        fig.suptitle('Computer Performance', fontsize=14, fontweight=600)

        self.df1.FrameRate.plot(title='Frame Rate '+self.df1_name, kind='hist', ax=axes[0, 0], bins=25, xlabel='frames per second', yticks=[], ylabel='')
        self.df2.FrameRate.plot(title='Frame Rate '+self.df2_name, kind='hist', ax=axes[0, 1], bins=25, xlabel='frames per second', yticks=[], ylabel='')
        self.df1.GpuUsage.plot(title='GPU Usage '+self.df1_name, kind='hist', ax=axes[1, 0], bins=25, xlabel='Percent of available thread took with a 1 sec avg', yticks=[], ylabel='')
        self.df2.GpuUsage.plot(title='GPU Usage '+self.df2_name, kind='hist', ax=axes[1, 1], bins=25, xlabel='Percent of available thread took with a 1 sec avg', yticks=[], ylabel='')
        self.df1.CpuUsageFG.plot(title='CPU Usage FG '+self.df1_name, kind='hist', ax=axes[2, 0], bins=25, xlabel='Percent of available tim fg thread took with a 1 sec avg', yticks=[], ylabel='')
        self.df2.CpuUsageFG.plot(title='CPU Usage FG '+self.df2_name, kind='hist', ax=axes[2, 1], bins=25, xlabel='Percent of available tim fg thread took with a 1 sec avg', yticks=[], ylabel='')
        self.df1.CpuUsageBG.plot(title ='CPU Usage BG '+self.df1_name, kind='hist', ax=axes[3, 0], bins=25, xlabel='Percent of available tim bg thread took with a 1 sec avg', yticks=[], ylabel='')
        self.df2.CpuUsageBG.plot(title ='CPU Usage BG '+self.df2_name, kind='hist', ax=axes[3, 1], bins=25, xlabel='Percent of available tim bg thread took with a 1 sec avg', yticks=[], ylabel='')

        plt.tight_layout()
        return fig


    def get_general_conditions_graph(self):

        fig, axes = plt.subplots(5, 2, figsize=(8,14), sharey='row')
        fig.suptitle('General Conditions', fontsize=14, fontweight=600)

        self.df1.TrackTemp.plot(title='Track Temp '+self.df1_name, kind='line', ax=axes[0, 0], xlabel='Session Progress', xticks=[], ylabel='°C')
        self.df2.TrackTemp.plot(title='Track Temp '+self.df2_name, kind='line', ax=axes[0, 1], xlabel='Session Progress', xticks=[], ylabel='°C')
        self.df1.AirTemp.plot(title='Air Temp '+self.df1_name, kind='line', ax=axes[1, 0], xlabel='Session Progress', xticks=[], ylabel='°C')
        self.df2.AirTemp.plot(title='Air Temp '+self.df2_name, kind='line', ax=axes[1, 1], xlabel='Session Progress', xticks=[], ylabel='°C')
        self.df1.AirDensity.plot(title='Air Density '+self.df1_name, kind='line', ax=axes[2, 0], xlabel='Session Progress', xticks=[], ylabel='kg/m^3')
        self.df2.AirDensity.plot(title='Air Density '+self.df2_name, kind='line', ax=axes[2, 1], xlabel='Session Progress', xticks=[], ylabel='kg/m^3')
        self.df1.AirPressure.plot(title='Air Pressure '+self.df1_name, kind='line', ax=axes[3, 0], xlabel='Session Progress', xticks=[], ylabel='mmHg')
        self.df2.AirPressure.plot(title='Air Pressure '+self.df2_name, kind='line', ax=axes[3, 1], xlabel='Session Progress', xticks=[], ylabel='mmHg')
        self.df1.RelativeHumidity.plot(title='Relative Humidity '+self.df1_name, kind='line', ax=axes[4, 0], xlabel='Session Progress', xticks=[], ylabel='%')
        self.df2.RelativeHumidity.plot(title='Relative Humidity '+self.df2_name, kind='line', ax=axes[4, 1], xlabel='Session Progress', xticks=[], ylabel='%')

        plt.tight_layout()
        return fig


    def get_car_setup_graph(self):

        fig, axes = plt.subplots(5, 2, figsize=(8,15), sharey='row')
        fig.suptitle('Car Setup', fontsize=14, fontweight=600)

        self.df1.dcABS.plot(title='ABS '+self.df1_name, kind='line', ax=axes[0, 0], xlabel='Session Progress', xticks=[], ylabel='Setting', drawstyle='steps-mid')
        self.df2.dcABS.plot(title='ABS '+self.df2_name, kind='line', ax=axes[0, 1], xlabel='Session Progress', xticks=[], ylabel='Setting', drawstyle='steps-mid')
        self.df1.dcTractionControl.plot(title='Traction Control '+self.df1_name, kind='line', ax=axes[1, 0], xlabel='Session Progress', xticks=[], ylabel='Setting', drawstyle='steps-mid')
        self.df2.dcTractionControl.plot(title='Traction Control '+self.df2_name, kind='line', ax=axes[1, 1], xlabel='Session Progress', xticks=[], ylabel='Setting', drawstyle='steps-mid')
        self.df1.dcBrakeBias.plot(title='Brake Bias '+self.df1_name, kind='line', ax=axes[2, 0], xlabel='Session Progress', xticks=[], ylabel='Setting', drawstyle='steps-mid')
        self.df2.dcBrakeBias.plot(title='Brake Bias '+self.df2_name, kind='line', ax=axes[2, 1], xlabel='Session Progress', xticks=[], ylabel='Setting', drawstyle='steps-mid')
        self.df1.PlayerTireCompound.plot(title='Tire Compound '+self.df1_name, kind='line', ax=axes[3, 0], xlabel='Session Progress', xticks=[], ylabel='Compound', drawstyle='steps-mid')
        self.df2.PlayerTireCompound.plot(title='Tire Compound '+self.df2_name, kind='line', ax=axes[3, 1], xlabel='Session Progress', xticks=[], ylabel='Compound', drawstyle='steps-mid')
        df1_cold_pressure = [self.df1.LFcoldPressure.min()/100, self.df1.RFcoldPressure.min()/100, self.df1.LRcoldPressure.min()/100, self.df1.RRcoldPressure.min()/100]
        df2_cold_pressure = [self.df2.LFcoldPressure.min()/100, self.df2.RFcoldPressure.min()/100, self.df2.LRcoldPressure.min()/100, self.df2.RRcoldPressure.min()/100]
        min_abs = min([min(df1_cold_pressure), min(df2_cold_pressure)])
        max_abs = max([max(df1_cold_pressure), max(df2_cold_pressure)])

        axes[4, 0].set_title('Cold Tire Pressure ' + self.df1_name)
        axes[4, 0].set_ylim([min_abs * 0.97, max_abs * 1.03])
        axes[4, 0].set_ylabel('bar')
        axes[4, 0].bar([0, 1, 2, 3], df1_cold_pressure, tick_label=['LF', 'RF', 'LR', 'RR'])
        axes[4, 1].set_title('Cold Tire Pressure ' + self.df2_name)
        axes[4, 1].bar([0, 1, 2, 3], df2_cold_pressure, tick_label=['LF', 'RF', 'LR', 'RR'])    

        plt.tight_layout()
        return fig


    def get_fuel_graph(self):

        fig, axes = plt.subplots(3, 2, figsize=(8,10), sharey='row')
        fig.suptitle('Fuel Status', fontsize=14, fontweight=600)

        df1_fuel_level = self.df1.groupby('Lap').FuelLevel
        df2_fuel_level = self.df2.groupby('Lap').FuelLevel
        df1_fuel_use_per_lap = self.df1.groupby('Lap').FuelUsePerHour
        df2_fuel_use_per_lap = self.df2.groupby('Lap').FuelUsePerHour

        df1_fuel_level.mean().plot(title='Fuel Level '+self.df1_name, kind='line', ax=axes[0, 0], xlabel='Lap', ylabel='litres', drawstyle='steps-mid', label='per lap')
        axes[0, 0].plot(df1_fuel_level.mean().index, [df1_fuel_level.mean().mean()] * len(df1_fuel_level.mean().index), label='mean')
        axes[0, 0].legend(frameon=False)
        df2_fuel_level.mean().plot(title='Fuel Level '+self.df2_name, kind='line', ax=axes[0, 1], xlabel='Lap', ylabel='litres', drawstyle='steps-mid', label='per lap')
        axes[0, 1].plot(df2_fuel_level.mean().index, [df2_fuel_level.mean().mean()] * len(df2_fuel_level.mean().index), label='mean')
        axes[0, 1].legend(frameon=False)

        df1_fuel_use_per_lap.mean().plot(title='Fuel Consumption '+self.df1_name, kind='line', ax=axes[1, 0], xlabel='Lap', ylabel='litres per hour',drawstyle='steps-mid', label='per lap')
        axes[1, 0].plot(df1_fuel_use_per_lap.mean().index, [df1_fuel_use_per_lap.mean().mean()] * len(df1_fuel_use_per_lap.mean().index), label='mean')
        axes[1, 0].legend(frameon=False)
        df2_fuel_use_per_lap.mean().plot(title='Fuel Consumption '+self.df2_name, kind='line', ax=axes[1, 1], xlabel='Lap', ylabel='litres per hour',drawstyle='steps-mid', label='per lap')
        axes[1, 1].plot(df2_fuel_use_per_lap.mean().index, [df2_fuel_use_per_lap.mean().mean()] * len(df2_fuel_use_per_lap.mean().index), label='mean')
        axes[1, 1].legend(frameon=False)

        self.df1[self.df1.Lap == self.df1_fastest_lap].plot(title='Fuel consumption ' + self.df1_name + ': Fastest lap ' + str(self.df1_fastest_lap), ax=axes[2, 0], kind='scatter', x='Lat', y='Lon', s=50, c='FuelUsePerHour', cmap=mpl.colors.LinearSegmentedColormap.from_list("", ['maroon','brown', 'orange', 'yellow']))

        self.df2[self.df2.Lap == self.df2_fastest_lap].plot(title='Fuel consumption ' + self.df2_name + ': Fastest lap ' + str(self.df2_fastest_lap), ax=axes[2, 1], kind='scatter', x='Lat', y='Lon', s=50, c='FuelUsePerHour', cmap=mpl.colors.LinearSegmentedColormap.from_list("", ['maroon','brown', 'orange', 'yellow']))

        axes[2, 0].plot(self.df1.iloc[0]['Lat'], self.df1.iloc[0]['Lon'], "ro", label='start/finish line', ms=10)
        axes[2, 1].plot(self.df2.iloc[0]['Lat'], self.df2.iloc[0]['Lon'], "ro", label='start/finsih line', ms=10)

        for axe in [axes[2, 0], axes[2, 1]]:
            for value in 'top right left bottom'.split():
                axe.spines[value].set_visible(False)
            axe.set_xlabel('')
            axe.set_ylabel('')

        axes[2, 0].tick_params(left = False, right = False, labelleft = False, labelbottom = False, bottom = False)
        axes[2, 1].tick_params(left = False, right = False, labelleft = False, labelbottom = False, bottom = False)

        axes[2, 0].legend(frameon=False)
        axes[2, 1].legend(frameon=False)

        plt.tight_layout()
        return fig


    def get_tyre_pressure_graph(self):

        fig, axes = plt.subplots(5, 2, figsize=(8,15), sharey=True)
        fig.suptitle('Tyre pressure', fontsize=14, fontweight=600)

        (self.df1.LFpressure/100).plot(ax=axes[0,0], label='Left Front', title='Tyre Pressure ' + self.df1_name, xlabel='Session Progress', xticks=[], ylabel='bar or psi?')
        (self.df1.RFpressure/100).plot(ax=axes[0,0], label='Right Front')
        (self.df1.LRpressure/100).plot(ax=axes[0,0], label='Left Rear')
        (self.df1.RRpressure/100).plot(ax=axes[0,0], label='Right Rear')
        axes[0,0].legend(frameon=False)
        (self.df2.LFpressure/100).plot(ax=axes[0,1], label='Left Front', title='Tyre Pressure ' + self.df2_name, xlabel='Session Progress', xticks=[], ylabel='bar or psi?')
        (self.df2.RFpressure/100).plot(ax=axes[0,1], label='Right Front')
        (self.df2.LRpressure/100).plot(ax=axes[0,1], label='Left Rear')
        (self.df2.RRpressure/100).plot(ax=axes[0,1], label='Right Rear')
        axes[0,1].legend(frameon=False)

        (self.df1.groupby('Lap').LFpressure.max()/100).plot(ax=axes[1,0], drawstyle='steps-mid', title='Left Front Tyre ' + self.df1_name, label='max', ylabel='bar or psi?')
        (self.df1.groupby('Lap').LFpressure.mean()/100).plot(ax=axes[1,0], label='mean')
        (self.df1.groupby('Lap').LFpressure.min()/100).plot(ax=axes[1,0], drawstyle='steps-mid', label='min')
        (self.df2.groupby('Lap').LFpressure.max()/100).plot(ax=axes[1,1], drawstyle='steps-mid', title='Left Front Tyre ' + self.df2_name, label='max', ylabel='bar or psi?')
        (self.df2.groupby('Lap').LFpressure.mean()/100).plot(ax=axes[1,1], label='mean')
        (self.df2.groupby('Lap').LFpressure.min()/100).plot(ax=axes[1,1], drawstyle='steps-mid', label='min')
        axes[1,0].legend(frameon=False)

        (self.df1.groupby('Lap').RFpressure.max()/100).plot(ax=axes[2,0], drawstyle='steps-mid', title='Right Front Tyre ' + self.df1_name, label='max', ylabel='bar or psi?')
        (self.df1.groupby('Lap').RFpressure.mean()/100).plot(ax=axes[2,0], label='mean')
        (self.df1.groupby('Lap').RFpressure.min()/100).plot(ax=axes[2,0], drawstyle='steps-mid', label='min')
        (self.df2.groupby('Lap').RFpressure.max()/100).plot(ax=axes[2,1], drawstyle='steps-mid', title='Right Front Tyre ' + self.df2_name, label='max', ylabel='bar or psi?')
        (self.df2.groupby('Lap').RFpressure.mean()/100).plot(ax=axes[2,1], label='mean')
        (self.df2.groupby('Lap').RFpressure.min()/100).plot(ax=axes[2,1], drawstyle='steps-mid', label='min')
        axes[2,0].legend(frameon=False)

        (self.df1.groupby('Lap').LRpressure.max()/100).plot(ax=axes[3,0], drawstyle='steps-mid', title='Left Rear Tyre ' + self.df1_name, label='max', ylabel='bar or psi?')
        (self.df1.groupby('Lap').LRpressure.mean()/100).plot(ax=axes[3,0], label='mean')
        (self.df1.groupby('Lap').LRpressure.min()/100).plot(ax=axes[3,0], drawstyle='steps-mid', label='min')
        (self.df2.groupby('Lap').LRpressure.max()/100).plot(ax=axes[3,1], drawstyle='steps-mid', title='Left Rear Tyre ' + self.df2_name, label='max', ylabel='bar or psi?')
        (self.df2.groupby('Lap').LRpressure.mean()/100).plot(ax=axes[3,1], label='mean')
        (self.df2.groupby('Lap').LRpressure.min()/100).plot(ax=axes[3,1], drawstyle='steps-mid', label='min')
        axes[3,0].legend(frameon=False)

        (self.df1.groupby('Lap').RRpressure.max()/100).plot(ax=axes[4,0], drawstyle='steps-mid', title='Right Rear Tyre ' + self.df1_name, label='max', ylabel='bar or psi?')
        (self.df1.groupby('Lap').RRpressure.mean()/100).plot(ax=axes[4,0], label='mean')
        (self.df1.groupby('Lap').RRpressure.min()/100).plot(ax=axes[4,0], drawstyle='steps-mid', label='min')
        (self.df2.groupby('Lap').RRpressure.max()/100).plot(ax=axes[4,1], drawstyle='steps-mid', title='Right Rear Tyre ' + self.df2_name, label='max', ylabel='bar or psi?')
        (self.df2.groupby('Lap').RRpressure.mean()/100).plot(ax=axes[4,1], label='mean')
        (self.df2.groupby('Lap').RRpressure.min()/100).plot(ax=axes[4,1], drawstyle='steps-mid', label='min')
        axes[4,0].legend(frameon=False)

        plt.tight_layout()
        return fig


    def get_tyre_temperature_graph(self):

        fig, axes = plt.subplots(5, 2, figsize=(8,15), sharey='row')
        fig.suptitle('Tyre temperature', fontsize=14, fontweight=600)

        self.df1['LFtempMean'] = (self.df1.LFtempL + self.df1.LFtempL + self.df1.LFtempR) / 3
        self.df1['RFtempMean'] = (self.df1.RFtempL + self.df1.RFtempL + self.df1.RFtempR) / 3
        self.df1['LRtempMean'] = (self.df1.LRtempL + self.df1.LRtempL + self.df1.LRtempR) / 3
        self.df1['RRtempMean'] = (self.df1.RRtempL + self.df1.RRtempL + self.df1.RRtempR) / 3
        self.df2['LFtempMean'] = (self.df2.LFtempL + self.df2.LFtempL + self.df2.LFtempR) / 3
        self.df2['RFtempMean'] = (self.df2.RFtempL + self.df2.RFtempL + self.df2.RFtempR) / 3
        self.df2['LRtempMean'] = (self.df2.LRtempL + self.df2.LRtempL + self.df2.LRtempR) / 3
        self.df2['RRtempMean'] = (self.df2.RRtempL + self.df2.RRtempL + self.df2.RRtempR) / 3

        self.df1.groupby('Lap')[['LFtempMean', 'RFtempMean', 'LRtempMean', 'RRtempMean']].mean().plot(ax=axes[0,0], title='Tyre Temp (mean) ' + self.df1_name,
                xlabel='Session Progress', xticks=[], ylabel='°C')
        axes[0,0].legend(labels=['Left Front', 'Right Front', 'Left Rear', 'Right Rear'], frameon=False, fontsize=8)
        self.df2.groupby('Lap')[['LFtempMean', 'RFtempMean', 'LRtempMean', 'RRtempMean']].mean().plot(ax=axes[0,1], title='Tyre Temp (mean) ' + self.df2_name,
                xlabel='Session Progress', xticks=[], ylabel='°C')
        axes[0,1].legend(labels=['Left Front', 'Right Front', 'Left Rear', 'Right Rear'], frameon=False, fontsize=8)

        df1_tyretemp_lf = self.df1.groupby('Lap')[['LFtempL', 'LFtempM', 'LFtempR']].mean()
        df2_tyretemp_lf = self.df2.groupby('Lap')[['LFtempL', 'LFtempM', 'LFtempR']].mean()
        tyretemp_lf_min = min(df1_tyretemp_lf.min().min(), df2_tyretemp_lf.min().min())
        tyretemp_lf_max = max(df1_tyretemp_lf.max().max(), df2_tyretemp_lf.max().max())
        df1_tyretemp_lf.plot(kind='bar', ax=axes[1,0], title='Tyre Temp Left Front ' + self.df1_name, 
                ylim=(tyretemp_lf_min * 0.98, tyretemp_lf_max * 1.02), ylabel='°C', xlabel='Lap')
        df2_tyretemp_lf.plot(kind='bar', ax=axes[1,1], title='Tyre Temp Left Front ' + self.df2_name,
                ylim=(tyretemp_lf_min * 0.98, tyretemp_lf_max * 1.02), xlabel='Lap')
        axes[1,0].legend(labels=['Left', 'Middle', 'Right'], frameon=False, fontsize=8)
        axes[1,1].legend(labels=['Left', 'Middle', 'Right'], frameon=False, fontsize=8)

        df1_tyretemp_rf = self.df1.groupby('Lap')[['RFtempL', 'RFtempM', 'RFtempR']].mean()
        df2_tyretemp_rf = self.df2.groupby('Lap')[['RFtempL', 'RFtempM', 'RFtempR']].mean()
        tyretemp_rf_min = min(df1_tyretemp_rf.min().min(), df2_tyretemp_rf.min().min())
        tyretemp_rf_max = max(df1_tyretemp_rf.max().max(), df2_tyretemp_rf.max().max())
        df1_tyretemp_rf.plot(kind='bar', ax=axes[2,0], title='Tyre Temp Right Front ' + self.df1_name, 
                ylim=(tyretemp_rf_min * 0.98, tyretemp_rf_max * 1.02), ylabel='°C', xlabel='Lap')
        df2_tyretemp_rf.plot(kind='bar', ax=axes[2,1], title='Tyre Temp Right Front ' + self.df2_name,
                ylim=(tyretemp_rf_min * 0.98, tyretemp_rf_max * 1.02), xlabel='Lap')
        axes[2,0].legend(labels=['Left', 'Middle', 'Right'], frameon=False, fontsize=8)
        axes[2,1].legend(labels=['Left', 'Middle', 'Right'], frameon=False, fontsize=8)

        df1_tyretemp_lr = self.df1.groupby('Lap')[['LRtempL', 'LRtempM', 'LRtempR']].mean()
        df2_tyretemp_lr = self.df2.groupby('Lap')[['LRtempL', 'LRtempM', 'LRtempR']].mean()
        tyretemp_lr_min = min(df1_tyretemp_lr.min().min(), df2_tyretemp_lr.min().min())
        tyretemp_lr_max = max(df1_tyretemp_lr.max().max(), df2_tyretemp_lr.max().max())
        df1_tyretemp_lr.plot(kind='bar', ax=axes[3,0], title='Tyre Temp Left Rear ' + self.df1_name, 
                ylim=(tyretemp_lr_min * 0.98, tyretemp_lr_max * 1.02), ylabel='°C', xlabel='Lap')
        df2_tyretemp_lr.plot(kind='bar', ax=axes[3,1], title='Tyre Temp Left Rear ' + self.df2_name,
                ylim=(tyretemp_lr_min * 0.98, tyretemp_lr_max * 1.02), xlabel='Lap')
        axes[3,0].legend(labels=['Left', 'Middle', 'Right'], frameon=False, fontsize=8)
        axes[3,1].legend(labels=['Left', 'Middle', 'Right'], frameon=False, fontsize=8)

        df1_tyretemp_rr = self.df1.groupby('Lap')[['RRtempL', 'RRtempM', 'RRtempR']].mean()
        df2_tyretemp_rr = self.df2.groupby('Lap')[['RRtempL', 'RRtempM', 'RRtempR']].mean()
        tyretemp_rr_min = min(df1_tyretemp_rr.min().min(), df2_tyretemp_rr.min().min())
        tyretemp_rr_max = max(df1_tyretemp_rr.max().max(), df2_tyretemp_rr.max().max())
        df1_tyretemp_rr.plot(kind='bar', ax=axes[4,0], title='Tyre Temp Right Rear ' + self.df1_name, 
                ylim=(tyretemp_rr_min * 0.98, tyretemp_rr_max * 1.02), ylabel='°C', xlabel='Lap')
        df2_tyretemp_rr.plot(kind='bar', ax=axes[4,1], title='Tyre Temp Right Rear ' + self.df2_name,
                ylim=(tyretemp_rr_min * 0.98, tyretemp_rr_max * 1.02), xlabel='Lap')
        axes[4,0].legend(labels=['Left', 'Middle', 'Right'], frameon=False, fontsize=8)
        axes[4,1].legend(labels=['Left', 'Middle', 'Right'], frameon=False, fontsize=8)

        plt.tight_layout()
        return fig

    
    def get_ride_height_graph(self):
        fig, axes = plt.subplots(4, 2, figsize=(8,15), sharey=True)
        fig.suptitle('Ride Height', fontsize=14, fontweight=600)


        (self.df1.groupby(by='Lap').LFrideHeight.max()*100).plot(ax=axes[0,0], drawstyle='steps-mid', label = 'max', ylabel='centimeter', title='Left Front Tyre ' + self.df1_name)
        (self.df1.groupby(by='Lap').LFrideHeight.mean()*100).plot(ax=axes[0,0], drawstyle='steps-mid', label = 'mean')
        (self.df1.groupby(by='Lap').LFrideHeight.min()*100).plot(ax=axes[0,0], drawstyle='steps-mid', label = 'mmin')
        axes[0,0].legend(frameon=False)

        (self.df2.groupby(by='Lap').LFrideHeight.max()*100).plot(ax=axes[0,1], drawstyle='steps-mid', label = 'max', ylabel='centimeter', title='Left Front Tyre ' + self.df2_name)
        (self.df2.groupby(by='Lap').LFrideHeight.mean()*100).plot(ax=axes[0,1], drawstyle='steps-mid', label = 'mean')
        (self.df2.groupby(by='Lap').LFrideHeight.min()*100).plot(ax=axes[0,1], drawstyle='steps-mid', label = 'mmin')


        (self.df1.groupby(by='Lap').RFrideHeight.max()*100).plot(ax=axes[1,0], drawstyle='steps-mid', label = 'max', ylabel='centimeter', title='Right Front Tyre ' + self.df1_name)
        (self.df1.groupby(by='Lap').RFrideHeight.mean()*100).plot(ax=axes[1,0], drawstyle='steps-mid', label = 'mean')
        (self.df1.groupby(by='Lap').RFrideHeight.min()*100).plot(ax=axes[1,0], drawstyle='steps-mid', label = 'mmin')
        axes[0,0].legend(frameon=False)

        (self.df2.groupby(by='Lap').RFrideHeight.max()*100).plot(ax=axes[1,1], drawstyle='steps-mid', label = 'max', ylabel='centimeter', title='Right Front Tyre ' + self.df2_name)
        (self.df2.groupby(by='Lap').RFrideHeight.mean()*100).plot(ax=axes[1,1], drawstyle='steps-mid', label = 'mean')
        (self.df2.groupby(by='Lap').RFrideHeight.min()*100).plot(ax=axes[1,1], drawstyle='steps-mid', label = 'mmin')


        (self.df1.groupby(by='Lap').LRrideHeight.max()*100).plot(ax=axes[2,0], drawstyle='steps-mid', label = 'max', ylabel='centimeter', title='Left Rear Tyre ' + self.df1_name)
        (self.df1.groupby(by='Lap').LRrideHeight.mean()*100).plot(ax=axes[2,0], drawstyle='steps-mid', label = 'mean')
        (self.df1.groupby(by='Lap').LRrideHeight.min()*100).plot(ax=axes[2,0], drawstyle='steps-mid', label = 'mmin')
        axes[0,0].legend(frameon=False)

        (self.df2.groupby(by='Lap').LRrideHeight.max()*100).plot(ax=axes[2,1], drawstyle='steps-mid', label = 'max', ylabel='centimeter', title='Left Rear Tyre ' + self.df2_name)
        (self.df2.groupby(by='Lap').LRrideHeight.mean()*100).plot(ax=axes[2,1], drawstyle='steps-mid', label = 'mean')
        (self.df2.groupby(by='Lap').LRrideHeight.min()*100).plot(ax=axes[2,1], drawstyle='steps-mid', label = 'mmin')


        (self.df1.groupby(by='Lap').RRrideHeight.max()*100).plot(ax=axes[3,0], drawstyle='steps-mid', label = 'max', ylabel='centimeter', title='Right Rear Tyre ' + self.df1_name)
        (self.df1.groupby(by='Lap').RRrideHeight.mean()*100).plot(ax=axes[3,0], drawstyle='steps-mid', label = 'mean')
        (self.df1.groupby(by='Lap').RRrideHeight.min()*100).plot(ax=axes[3,0], drawstyle='steps-mid', label = 'mmin')
        axes[0,0].legend(frameon=False)

        (self.df2.groupby(by='Lap').RRrideHeight.max()*100).plot(ax=axes[3,1], drawstyle='steps-mid', label = 'max', ylabel='centimeter', title='Right Rear Tyre ' + self.df2_name)
        (self.df2.groupby(by='Lap').RRrideHeight.mean()*100).plot(ax=axes[3,1], drawstyle='steps-mid', label = 'mean')
        (self.df2.groupby(by='Lap').RRrideHeight.min()*100).plot(ax=axes[3,1], drawstyle='steps-mid', label = 'mmin')

        plt.tight_layout()
        return fig
    

    def get_break_graph(self):
     
        fig, axes = plt.subplots(6, 2, figsize=(8,22), sharey='row')
        fig.suptitle('Brake Overview', fontsize=14, fontweight=600)


        # BRAKE Intensity Total
        sns.violinplot(data=self.df1[self.df1.Brake > 0], y='Brake', cut=0, inner=None, linewidth=1, color='green', ax=axes[0, 0])
        sns.violinplot(data=self.df2[self.df2.Brake > 0], y='Brake', cut=0, inner=None, linewidth=1, color='green', ax=axes[0, 1])
        axes[0, 0].set_title('Brake Intensity Total ' + self.df1_name)
        axes[0, 0].set_ylabel('Intensity in %')
        axes[0, 0].set_xlabel('Total Count')
        axes[0, 1].set_title('Brake Intensity Total ' + self.df2_name)
        axes[0, 1].set_xlabel('Total Count')


        # BRAKE Intesity Fastest Lap
        sns.violinplot(data=self.df1[(self.df1.Brake > 0) & (self.df1.Lap == self.df1_fastest_lap)], y='Brake', cut=0, inner=None, linewidth=1, color='green', ax=axes[1, 0])
        sns.violinplot(data=self.df2[(self.df2.Brake > 0) & (self.df2.Lap == self.df2_fastest_lap)], y='Brake', cut=0, inner=None, linewidth=1, color='green', ax=axes[1, 1])
        axes[1, 0].set_title('Brake Intensity ' + self.df1_name + ' fastet lap ' + str(self.df1_fastest_lap))
        axes[1, 0].set_ylabel('Intensity in %')
        axes[1, 0].set_xlabel('Total Count')
        axes[1, 1].set_title('Brake Intensity ' + self.df2_name + ' fastet lap ' + str(self.df2_fastest_lap))
        axes[1, 1].set_xlabel('Total Count')

        # BRAKE Intensity Lap Overview
        sns.violinplot(data=self.df1[self.df1.Brake > 0], x='Lap', y='Brake', cut=0, inner=None, linewidth=0, color='green', ax=axes[2, 0])
        sns.violinplot(data=self.df2[self.df2.Brake > 0], x='Lap', y='Brake', cut=0, inner=None, linewidth=0, color='green', ax=axes[2, 1])
        axes[2, 0].set_title('Brake Intensity ' + self.df1_name)
        axes[2, 0].set_ylabel('Intensity in %')
        axes[2, 1].set_title('Brake Intensity ' + self.df2_name)


        # BRAKE POINTS
        self.df1[self.df1.Lap == self.df1_fastest_lap].plot(title='Brake Points ' + self.df1_name + ': Fastest lap ' + str(self.df1_fastest_lap), ax=axes[3, 0], kind='scatter', x='Lat', y='Lon', s=50, c='Brake', cmap=mpl.colors.LinearSegmentedColormap.from_list("", ['maroon','brown', 'orange', 'yellow']))
        self.df2[self.df2.Lap == self.df2_fastest_lap].plot(title='Brake Points ' + self.df2_name + ': Fastest lap ' + str(self.df2_fastest_lap), ax=axes[3, 1], kind='scatter', x='Lat', y='Lon', s=50, c='Brake', cmap=mpl.colors.LinearSegmentedColormap.from_list("", ['maroon','brown', 'orange', 'yellow']))
        axes[3, 0].plot(self.df1.iloc[0]['Lat'], self.df1.iloc[0]['Lon'], "ro", label='start/finish line', ms=10)
        axes[3, 1].plot(self.df2.iloc[0]['Lat'], self.df2.iloc[0]['Lon'], "ro", label='start/finsih line', ms=10)
        for axe in [axes[3, 0], axes[3, 1]]:
            for value in 'top right left bottom'.split():
                axe.spines[value].set_visible(False)
            axe.set_xlabel('')
            axe.set_ylabel('')
        axes[3, 0].tick_params(left = False, right = False, labelleft = False, labelbottom = False, bottom = False)
        axes[3, 1].tick_params(left = False, right = False, labelleft = False, labelbottom = False, bottom = False)
        axes[3, 0].legend(frameon=False)
        axes[3, 1].legend(frameon=False)


        # ABS percentage
        x1 = list(self.df1.Lap.unique())
        y1 = []
        for lap in x1:
            denominator = self.df1[(self.df1.Lap == lap) & (self.df1.Brake > 0)].BrakeABSactive.count()
            numerator = self.df1[(self.df1.Lap == lap) & (self.df1.Brake > 0) & (self.df1.BrakeABSactive == 1)].BrakeABSactive.count()
            y1.append(numerator/denominator*100)

        x2 = list(self.df2.Lap.unique())
        y2 = []
        for lap in x2:
            denominator = self.df2[(self.df2.Lap == lap) & (self.df2.Brake > 0)].BrakeABSactive.count()
            numerator = self.df2[(self.df2.Lap == lap) & (self.df2.Brake > 0) & (self.df2.BrakeABSactive == 1)].BrakeABSactive.count()
            y2.append(numerator/denominator*100)

        axes[4,0].bar(x=x1, height=y1, label='ABS pct.', color='green')
        axes[4,0].plot(x1, [(sum(y1) / len(y1))]*len(x1), color='red', label='mean')
        axes[4,0].set_title('ABS usage ' + self.df1_name)
        axes[4,0].set_ylabel('Break under ABS in %')
        axes[4,0].set_xlabel('Lap')
        axes[4,1].bar(x=x2, height=y2)
        axes[4,1].plot(x2, [(sum(y2) / len(y2))]*len(x2), color='red', label='mean')
        axes[4,1].set_title('ABS usage ' + self.df2_name)
        axes[4,1].set_xlabel('Lap')
        axes[4,1].bar(x=x2, height=y2, color='green')
        axes[4,0].legend(frameon=False)

        y_min = min(min(y1), min(y2))
        y_max = max(max(y1), max(y2))
        axes[4,0].set_ylim(y_min * 0.90 , y_max * 1.10)


        # ABS BRAKE POINTS
        self.df1[self.df1.Lap == self.df1_fastest_lap].plot(title='ABS Brake Points ' + self.df1_name + ': Fastest lap ' + str(self.df1_fastest_lap), ax=axes[5, 0], kind='scatter', x='Lat', y='Lon', s=50, c='BrakeABSactive', cmap=mpl.colors.LinearSegmentedColormap.from_list("", ['maroon','brown', 'orange', 'yellow']))
        self.df2[self.df2.Lap == self.df2_fastest_lap].plot(title='ABS Brake Points ' + self.df2_name + ': Fastest lap ' + str(self.df2_fastest_lap), ax=axes[5, 1], kind='scatter', x='Lat', y='Lon', s=50, c='BrakeABSactive', cmap=mpl.colors.LinearSegmentedColormap.from_list("", ['maroon','brown', 'orange', 'yellow']))
        axes[5, 0].plot(self.df1.iloc[0]['Lat'], self.df1.iloc[0]['Lon'], "ro", label='start/finish line', ms=10)
        axes[5, 1].plot(self.df2.iloc[0]['Lat'], self.df2.iloc[0]['Lon'], "ro", label='start/finsih line', ms=10)
        for axe in [axes[5, 0], axes[5, 1]]:
            for value in 'top right left bottom'.split():
                axe.spines[value].set_visible(False)
            axe.set_xlabel('')
            axe.set_ylabel('')
        axes[5, 0].tick_params(left = False, right = False, labelleft = False, labelbottom = False, bottom = False)
        axes[5, 1].tick_params(left = False, right = False, labelleft = False, labelbottom = False, bottom = False)
        axes[5, 0].legend(frameon=False)
        axes[5, 1].legend(frameon=False)
        plt.tight_layout()
        return fig











