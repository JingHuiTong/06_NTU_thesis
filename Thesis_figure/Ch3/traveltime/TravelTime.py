from obspy.taup import plot_travel_times
from obspy.taup import TauPyModel
import matplotlib.pyplot as plt

model = TauPyModel(model="iasp91")

fig, ax = plt.subplots(figsize=(5, 7))
ax = plot_travel_times(source_depth=300, phase_list=['PcS','PS','PKS',"SKS",'S','ScS', "SKKS"],
                       ax=ax, fig=fig, verbose=True, legend=True)
                       
                       
fig.savefig('TravelTime_300km.png',dpi=200)
fig.savefig('TravelTime_300km.pdf',dpi=200)

