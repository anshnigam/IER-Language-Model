# d1 = "Chandrayan, series of Indian lunar space probes. Chandrayan (Chandrayan is Hindi for “moon craft”), the first lunar space probe of the Indian Space Research Organisation (ISRO), found water on the Moon. It mapped the Moon in infrared, visible, and X-ray light from lunar orbit and used reflected radiation to prospect for various elements, minerals, and ice. It operated in 2008 09. Chandrayan 2, which launched in 2019, was designed to be ISRO first lunar lander. Chandrayan 3 was ISRO first lunar lander and touched down in the Moon south polar region in 2023."
# d2 = "A Polar Satellite Launch Vehicle launched the 590-kg (1,300-pound) Chandrayan 1 on October 22, 2008, from the Satish Dhawan Space Centre on Sriharikota Island, Andhra Pradesh state. The probe then was boosted into an elliptical polar orbit around the Moon, 504 km (312 miles) high at its closest to the lunar surface and 7,502 km (4,651 miles) at its farthest. After checkout, it descended to a 100-km (60-mile) orbit. On November 14, 2008, Chandrayan 1 launched a small craft, the Moon Impact Probe (MIP), that was designed to test systems for future landings and study the thin lunar atmosphere before crashing on the Moon surface. MIP impacted near the south pole, but, before it crashed, it discovered small amounts of water in the Moon atmosphere."
# d3 = "The U.S. National Aeronautics and Space Administration (NASA) contributed two instruments, the Moon Mineralogy Mapper (M3) and the Miniature Synthetic Aperture Radar (Mini-SAR), which sought ice at the poles. M3 studied the lunar surface in wavelengths from the visible to the infrared in order to isolate signatures of different minerals on the surface. It found small amounts of water and hydroxyl radicals on the Moon surface. M3 also discovered in a crater near the Moon equator evidence for water coming from beneath the surface. Mini-SAR broadcast polarized radio waves at the north and south polar regions. Changes in the polarization of the echo measured the dielectric constant and porosity, which are related to the presence of water ice. The European Space Agency (ESA) had two other experiments, an infrared spectrometer and a solar wind monitor. The Bulgarian Aerospace Agency provided a radiation monitor."
# d4 = "The principal instruments from ISRO—the Terrain Mapping Camera, the HyperSpectral Imager, and the Lunar Laser Ranging Instrument—produced images of the lunar surface with high spectral and spatial resolution, including stereo images with a 5-metre (16-foot) resolution and global topographic maps with a resolution of 10 metres (33 feet). The Chandrayan Imaging X-ray Spectrometer, developed by ISRO and ESA, was designed to detect magnesium, aluminum, silicon, calcium, titanium, and iron by the X-rays they emit when exposed to solar flares. This was done in part with the Solar X-Ray Monitor, which measured incoming solar radiation."
# d5 = "Chandrayaan 1 operations were originally planned to last two years, but the mission ended on August 28, 2009, when radio contact was lost with the spacecraft.Chandrayaan2 launched on July 22, 2019, from Sriharikota on a Geosynchronous Satellite Launch Vehicle Mark III. The spacecraft consisted of an orbiter, a lander, and a rover. The orbiter circles the Moon in a polar orbit at a height of 100 km (62 miles) and has a planned mission lifetime of seven and a half years. The mission Vikram lander (named after ISRO founder Vikram Sarabhai) was planned to land on September 7. Vikram carried the small (27 kg) Pragyan (Sanskrit: “Wisdom”) rover. Both Vikram and Pragyan were designed to operate for 1 lunar day (14 Earth days). However, just before Vikram was to touch down on the Moon, contact was lost at an altitude of 2 km (1.2 miles)."
# d6 = "Chandrayan 3 launched from Sriharikota on July 14, 2023. The spacecraft consists of a Vikram lander and a Pragyan rover. The Vikram lander touched down on the Moon on August 23. It became the first spacecraft to land in the Moon south polar region where water ice could be found under the surface. The landing site was the farthest south that any lunar probe had touched down, and India was the fourth country to have landed a spacecraft on the Moon—after the United States, Russia, and China."

# documents = [d1,d2,d3,d4,d5,d6]
# query = "Chandrayan 3 had a Vikram lander and Rover."

import math
import re

def tokenize(doc: str):
    doc = re.sub(r'[^\w\s]', '', doc)
    return doc.lower().split()

def fill_freqs(freqs: dict, d: dict, dnum: int, N: int):
    for i in d[dnum]:
        if i in freqs:
            freqs[i][dnum-1] += 1
        else:
            freqs[i] = [0]*(N+1)
            freqs[i][dnum-1] = 1

def fill_last_col(freqs: dict,N: int):
    for i in freqs:
        sum=0
        for j in range(N):
            sum += freqs[i][j]
        freqs[i][N] = sum

def fill_fj(freqs: dict,fj: list[float],N: int):
    for i in freqs:
        for j in range(N+1):
            fj[j] += freqs[i][j]

def calc_smop(smop: dict,q_list: list[str],freqs: dict,fj: list[float],N: int):
    for i in q_list:
        smop[i] = [0.0]*N
        for j in range(N):
            if i in d[j+1]:
                smop[i][j] = 0.4*(freqs[i][j]/fj[j]) + 0.6*(freqs[i][N]/fj[N])

def calc_pkc(pkc: dict,q_list: list[str],freqs: dict,fj: list[float],N: int):
    for i in q_list:
        pkc[i] = freqs[i][N]/fj[N]

def calc_alpha(alpha: list[float],q_list: list[str],smop: dict,pkc: dict,N: int):
    for j in range(N):
        sum_num = 0
        sum_den = 0
        for i in q_list:
            sum_num += smop[i][j]
            sum_den += pkc[i]
        alpha[j] = (1-sum_num)/(1-sum_den)

def calc_pki(q_list: list[str],pki: dict,d: dict,smop: dict,alpha: list[float],pkc: dict,N: int):
    for i in q_list:
        pki[i] = [0.0]*N
        for j in range(N):
            if i in d[j+1]:
                pki[i][j] = smop[i][j]
            else:
                pki[i][j] = alpha[j]*pkc[i]

def calc_logpro(q_list,d,pki,pkc,alpha,j,logpro):
    sum = 0
    for i in q_list:
        if i in d[j+1]:
            sum += math.log2(pki[i][j]/(alpha[j]*pkc[i]))
    sum += len(q_list)*math.log2(alpha[j])
    logpro[j] = sum


d = dict()
freqs = dict()
smop = dict()
pkc = dict()
pki = dict()

print("Enter number of docx: ")
N = int(input())

for i in range(1,N+1):
    print(f"Enter docx {i}: ")
    text = input()
    d[i] = tokenize(text)
    fill_freqs(freqs,d,i,N)

fill_last_col(freqs,N)

fj = [0]*(N+1)
fill_fj(freqs,fj,N)

print("Enter query:")
q = input()
q_list = tokenize(q)

calc_smop(smop,q_list,freqs,fj,N)
calc_pkc(pkc,q_list,freqs,fj,N)

alpha = [0.0]*(N)
calc_alpha(alpha,q_list,smop,pkc,N)

calc_pki(q_list,pki,d,smop,alpha,pkc,N)

logpro = [0.0]*(N)
for j in range(N):
    calc_logpro(q_list,d,pki,pkc,alpha,j,logpro)

pro = [2**(-i) for i in logpro]
rank= []
for j in range(1,N+1):
    rank.append(["Document "+str(j),pro[j-1]])
rank.sort(key=lambda x:x[1],reverse=True)
for j in range(N):
    print(f"Rank {j+1}: {rank[j][0]}")


# print(f"Freqs: {freqs}")
# print(f"fj: {fj}")
# print(f"smoothened probability: {smop}")
# print(f"P(Ki|C): {pkc}")
# print(f"alpha: {alpha}")
# print(f"P(ki|Mj): {pki}")
# print(f"probability: {[2**(-i) for i in logpro]}")