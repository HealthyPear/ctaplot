"""
ana.py
======
Contain mathematical functions to make results analysis
(compute angular resolution, effective surface, energy resolution... )
"""


import numpy as np
import ctaplot.dataset as ds
from scipy.stats import binned_statistic

class irf_cta:
    """
    Class to handle Instrument Response Function data
    """
    def __init__(self):
        self.site = ''
        self.E_bin = np.logspace(np.log10(2.51e-02), 2, 19)
        self.E = logbin_mean(self.E_bin)

        # Area of CTA sites in meters
        self.ParanalArea_prod3 = 19.63e6
        self.LaPalmaArea_prod3 = 11341149 #6.61e6

    def set_E_bin(self, E_bin):
        self.E_bin = E_bin
        self.E = logbin_mean(self.E_bin)


class cta_performances:
    def __init__(self):
        self.site = ''
        self.E = np.empty(0)
        self.effective_area = np.empty(0)
        self.angular_resolution = np.empty(0)
        self.energy_resolution = np.empty(0)
        self.sensitivity = np.empty(0)

    def get_effective_area(self, observation_time=50):
        """
        Return the effective area at the given observation time in hours.
        NB: Only 50h supported
        Returns the energy array and the effective area array
        Parameters
        ----------
        observation_time: optional

        Returns
        -------
        `numpy.ndarray`, `numpy.ndarray`
        """
        if self.site == 'south':
            if observation_time == 50:
                self.E, self.effective_area = np.loadtxt(
                    ds.get('CTA-Performance-prod3b-v1-South-20deg-50h-EffArea.txt'),
                    skiprows=11, unpack=True)
            if observation_time == 0.5:
                self.E, self.effective_area = np.loadtxt(
                    ds.get('CTA-Performance-prod3b-v1-North-20deg-30m-EffArea.txt'),
                    skiprows=11, unpack=True)

        if self.site == 'north':
            if observation_time == 50:
                self.E, self.effective_area = np.loadtxt(
                    ds.get('CTA-Performance-prod3b-v1-North-20deg-50h-EffArea.txt'),
                    skiprows=11, unpack=True)
            if observation_time == 0.5:
                self.E, self.effective_area = np.loadtxt(
                    ds.get('CTA-Performance-prod3b-v1-North-20deg-30m-EffArea.txt'),
                    skiprows=11, unpack=True)
        return self.E, self.effective_area

    def get_angular_resolution(self):
        if self.site == 'south':
            self.E, self.angular_resolution = np.loadtxt(
                ds.get('CTA-Performance-prod3b-v1-South-20deg-50h-Angres.txt'),
                skiprows=11, unpack=True)
        if self.site == 'north':
            self.E, self.angular_resolution = np.loadtxt(
                ds.get('CTA-Performance-prod3b-v1-North-20deg-50h-Angres.txt'),
                skiprows=11, unpack=True)

        return self.E, self.angular_resolution

    def get_energy_resolution(self):
        if self.site in ['south', 'paranal']:
            self.E, self.energy_resolution = np.loadtxt(ds.get('CTA-Performance-prod3b-v1-South-20deg-50h-Eres.txt'),
                                                        skiprows=11, unpack=True)
        if self.site in ['north', 'lapalma']:
            self.E, self.energy_resolution = np.loadtxt(ds.get('CTA-Performance-prod3b-v1-North-20deg-50h-Eres.txt'),
                                                        skiprows=11, unpack=True)

        return self.E, self.energy_resolution

    def get_sensitivity(self, observation_time=50):
        if self.site in ['south', 'paranal']:
            Emin, Emax, self.sensitivity = np.loadtxt(ds.get('CTA-Performance-prod3b-v1-South-20deg-50h-DiffSens.txt'),
                                                  skiprows=10, unpack=True)
            self.E = logbin_mean(np.append(Emin, Emax[-1]))

        if self.site in ['north', 'lapalma']:
            Emin, Emax, self.sensitivity = np.loadtxt(ds.get('CTA-Performance-prod3b-v1-North-20deg-50h-DiffSens.txt'),
                                                  skiprows=10, unpack=True)
            self.E = logbin_mean(np.append(Emin, Emax[-1]))

        return self.E, self.sensitivity



class cta_requirements:
    def __init__(self):
        self.site = ''
        self.E = np.empty(0)
        self.effective_area = np.empty(0)
        self.angular_resolution = np.empty(0)
        self.energy_resolution = np.empty(0)
        self.sensitivity = np.empty(0)

    def get_effective_area(self, observation_time=50):
        """
        Return the effective area at the given observation time in hours.
        NB: Only 0.5h supported
        Returns the energy array and the effective area array
        Parameters
        ----------
        observation_time: optional

        Returns
        -------
        `numpy.ndarray`, `numpy.ndarray`
        """
        if self.site == 'south':
            self.E, self.effective_area = np.loadtxt(ds.get('cta_requirements_South-30m-EffectiveArea.dat'),
                                                     unpack=True)
        if self.site == 'north':
            self.E, self.effective_area = np.loadtxt(ds.get('cta_requirements_North-30m-EffectiveArea.dat'),
                                                     unpack=True)

        return self.E, self.effective_area

    def get_angular_resolution(self):
        if self.site == 'south':
            self.E, self.angular_resolution = np.loadtxt(ds.get('cta_requirements_South-50h-AngRes.dat'), unpack=True)
        if self.site == 'north':
            self.E, self.angular_resolution = np.loadtxt(ds.get('cta_requirements_North-50h-AngRes.dat'), unpack=True)

        return self.E, self.angular_resolution

    def get_energy_resolution(self):
        if self.site in ['south', 'paranal']:
            self.E, self.energy_resolution = np.loadtxt(ds.get('cta_requirements_South-50h-ERes.dat'), unpack=True)
        if self.site in ['north', 'lapalma']:
            self.E, self.energy_resolution = np.loadtxt(ds.get('cta_requirements_North-50h-ERes.dat'), unpack=True)

        return self.E, self.energy_resolution

    def get_sensitivity(self, observation_time=50):
        if self.site in ['south', 'paranal']:
            self.E, self.sensitivity = np.loadtxt(ds.get('cta_requirements_South-50h.dat'), unpack=True)
        if self.site in ['north', 'lapalma']:
            self.E, self.sensitivity = np.loadtxt(ds.get('cta_requirements_North-50h.dat'), unpack=True)

        return self.E, self.sensitivity



def logspace_decades_nbin(Xmin, Xmax, n=5):
    """
    return an array with logspace and n bins / decade
    Parameters
    ----------
    Xmin: float
    Xmax: float
    n: int - number of bins per decade

    Returns
    -------
    1D Numpy array
    """
    ei = np.int(np.log10(Xmin))
    ea = np.int(np.floor(np.log10(Xmax)) + 1*(np.log10(Xmax) > np.floor(np.log10(Xmax))))
    return np.logspace(ei, ea, n * (ea-ei)+1)



def stat_per_energy(energy, y, statistic='mean'):
    """
    Return statistic for the given quantity per energy bins.
    The binning is given by irf_cta

    Parameters
    ----------
    energy: `numpy.ndarray` (1d)
        event energies
    y: `numpy.ndarray` (1d)
    statistic: string
        see `scipy.stat.binned_statistic`

    Returns
    -------
    `numpy.ndarray, numpy.ndarray, numpy.ndarray`
        bin_stat, bin_edges, binnumber
    """

    irf = irf_cta()

    bin_stat, bin_edges, binnumber = binned_statistic(energy, y, statistic=statistic, bins=irf.E)

    return bin_stat, bin_edges, binnumber



def bias(simu, reco):
    """
    Compute the bias of a reconstructed variable.

    Parameters
    ----------
    simu: `numpy.ndarray`
    reco: `numpy.ndarray`

    Returns
    -------
    float
    """
    assert len(simu) == len(reco), "both arrays should have the same size"
    res = (reco - simu) / reco
    return np.median(res)


def resolution(simu, reco, percentile=68.27, error_percentile=68.27, bias_correction=False):
    """
    Compute the resolution of reco as the Qth (68.27 as standard = 1 sigma) containment radius of (simu-reco)/reco
    with the lower and upper confidence limits defined the values inside the error_percentile

    Parameters
    ----------
    simu: `numpy.ndarray` (1d)
        simulated quantity
    reco: `numpy.ndarray` (1d)
        reconstructed quantity
    percentile: float
        percentile for the resolution containment radius
    error_percentile: float
        percentile for the confidence limits
    bias_correction: bool
        if True, the resolution is corrected with the bias computed on simu and reco

    Returns
    -------
    `numpy.ndarray` - [resolution, lower_confidence_limit, upper_confidence_limit]
    """
    assert len(simu) == len(reco), "both arrays should have the same size"

    b = bias(simu, reco) if bias_correction else 0

    res = np.abs((reco - simu) / reco - b)
    return np.append(RQ(res, percentile), percentile_confidence_interval(res, percentile=error_percentile))


def resolution_per_energy(simu, reco, SimuE, bias_correction=False):
    """
    Parameters
    ----------
    simu: 1d `numpy.ndarray` of simulated energies
    reco: 1d `numpy.ndarray` of reconstructed energies

    Returns
    -------
    (e, res) : tuple of 1d numpy arrays - energy, resolution
    """
    res = []
    irf = irf_cta()
    for i, e in enumerate(irf.E):
        mask = (SimuE > irf.E_bin[i]) & (SimuE < irf.E_bin[i+1])
        res.append(resolution(simu[mask], reco[mask], bias_correction=bias_correction))

    return irf.E_bin, np.array(res)


def energy_resolution(true_energy, reco_energy, percentile=68.27, error_percentile=68.27, bias_correction=False):
    """
    Compute the energy resolution of RecoE as the Qth (68 as standard) containment radius of DeltaE/E
    with the lower and upper confidence limits

    Parameters
    ----------
    true_energy: 1d numpy array of simulated energies
    reco_energy: 1d numpy array of reconstructed energies
    percentile: float
        <= 100

    Returns
    -------
    `numpy.array` - [energy_resolution, lower_confidence_limit, upper_confidence_limit]
    """
    return resolution(true_energy, reco_energy, percentile=percentile,
                      error_percentile=error_percentile, bias_correction=bias_correction)


def energy_res_per_energy(SimuE, RecoE, bias_correction=False):
    """

    Parameters
    ----------
    SimuE: 1d numpy array of simulated energies
    RecoE: 1d numpy array of reconstructed energies

    Returns
    -------
    (e, e_res) : tuple of 1d numpy arrays - energy, resolution in energy
    """
    resE = []
    irf = irf_cta()
    for i, e in enumerate(irf.E):
        mask = (SimuE > irf.E_bin[i]) & (SimuE < irf.E_bin[i+1])
        resE.append(energy_resolution(SimuE[mask], RecoE[mask], bias_correction=bias_correction))


    return irf.E_bin, np.array(resE)


def energy_bias(SimuE, RecoE):
    """
    Compute the energy bias per energy bin.
    Parameters
    ----------
    SimuE: 1d numpy array of simulated energies
    RecoE: 1d numpy array of reconstructed energies

    Returns
    -------
    (e, biasE) : tuple of 1d numpy arrays - energy, energy bias
    """
    biasE = []
    irf = irf_cta()
    for i, e in enumerate(irf.E):
        mask = (SimuE > irf.E_bin[i]) & (SimuE < irf.E_bin[i+1])
        biasE.append(bias(SimuE[mask], RecoE[mask]))

    return irf.E_bin, np.array(biasE)



def get_angles_pipi(angles):
    """
    return angles modulo between -pi and +pi

    Parameters
    ----------
    angles: `numpy.ndarray`

    Returns
    -------
    `numpy.ndarray`
    """
    return np.mod(angles + np.pi, 2 * np.pi) - np.pi


def get_angles_0pi(angles):
    """
    return angles modulo between 0 and +pi

    Parameters
    ----------
    angles: `numpy.ndarray`

    Returns
    -------
    `numpy.ndarray`
    """
    return np.mod(angles, np.pi)


def theta2(RecoAlt, RecoAz, AltSource, AzSource):
    """
    Compute the theta2 in radians

    Parameters
    ----------
    RecoAlt: 1d `numpy.ndarray` - reconstructed Altitude in radians
    RecoAz: 1d `numpy.ndarray` - reconstructed Azimuth in radians
    AltSource: 1d `numpy.ndarray` - true Altitude in radians
    AzSource: 1d `numpy.ndarray` -  true Azimuth in radians

    Returns
    -------
    1d `numpy.ndarray`
    """
    assert (len(RecoAz) == len(RecoAlt))
    assert (len(RecoAlt) == len(AltSource))
    if len(RecoAlt) == 0:
        return np.empty(0)
    else:
        return angular_separation_altaz(RecoAlt, RecoAz, AltSource, AzSource)**2


def angular_resolution(RecoAlt, RecoAz, SimuAlt, SimuAz, Q = 68, conf=1.645):
    """
    Compute the angular resolution as the Qth (standard being 68)
    containment radius of theta2 with lower and upper limits on this value
    corresponding to the confidence value required (1.645 for 95% confidence)

    Parameters
    ----------
    RecoAlt: `numpy.ndarray` - reconstructed altitude angle in radians
    RecoAz: `numpy.ndarray` - reconstructed azimuth angle in radians
    SimuAlt: `numpy.ndarray` - true altitude angle in radians
    SimuAz: `numpy.ndarray` - true azimuth angle in radians
    Q: float - percentile, 68 corresponds to one sigma
    conf: float

    Returns
    -------
    `numpy.array` [angular_resolution, lower limit, upper limit]
    """
    t2 = np.sort(theta2(RecoAlt, RecoAz, SimuAlt, SimuAz))

    ang_res = RQ(t2, Q)
    percentile_confidence_interval(t2, Q, conf)
    return np.sqrt(np.append(ang_res, percentile_confidence_interval(t2, Q, conf)))


def angular_resolution_per_energy(RecoAlt, RecoAz, SimuAlt, SimuAz, Energy, **kwargs):
    """
    Plot the angular resolution as a function of the event simulated energy

    Parameters
    ----------
    RecoAlt: `numpy.ndarray`
    RecoAz: `numpy.ndarray`
    SimuAlt: `numpy.ndarray`
    SimuAz: `numpy.ndarray`
    Energy: `numpy.ndarray`
    **kwargs: args for `angular_resolution`

    Returns
    -------
    (E, RES) : (1d numpy array, 1d numpy array) = Energies, Resolution
    """
    assert len(RecoAlt) == len(Energy)
    assert len(Energy) > 0, "Empty arrays"

    irf = irf_cta()

    E_bin = irf.E_bin
    RES = []

    for i, e in enumerate(E_bin[:-1]):
        mask = (Energy > E_bin[i]) & (Energy <= E_bin[i+1])
        RES.append(angular_resolution(RecoAlt[mask], RecoAz[mask], SimuAlt[mask], SimuAz[mask], **kwargs))

    return E_bin, np.array(RES)


def effective_area(SimuE, RecoE, simuArea):
    """
    Compute the effective area from a list of simulated energies and reconstructed energies
    Parameters
    ----------
    SimuE: 1d numpy array
    RecoE: 1d numpy array
    simuArea: float - area on which events are simulated
    Returns
    -------
    float = effective area
    """
    return simuArea * len(RecoE)/len(SimuE)


def effective_area_per_energy(SimuE, RecoE, simuArea):
    """
    Compute the effective area per energy bins from a list of simulated energies and reconstructed energies

    Parameters
    ----------
    SimuE: 1d numpy array
    RecoE: 1d numpy array
    simuArea: float - area on which events are simulated

    Returns
    -------
    (E, Seff) : (1d numpy array, 1d numpy array)
    """

    irf = irf_cta()

    count_R, bin_R = np.histogram(RecoE, bins=irf.E_bin)
    count_S, bin_S = np.histogram(SimuE, bins=irf.E_bin)

    np.seterr(divide='ignore', invalid='ignore')
    return irf.E_bin, np.nan_to_num(simuArea * count_R/count_S)


def mask_range(X, Xmin=0, Xmax=np.inf):
    """
    create a mask for X to get values between Xmin and Xmax
    Parameters
    ----------
    X: 1d numpy array
    Xmin: float
    Xmax: float

    Returns
    -------
    1d numpy array of boolean
    """
    mask = (X > Xmin) & (X < Xmax)
    return mask


def angles_modulo_degrees(RecoAlt, RecoAz, SimuAlt, SimuAz):
    RecoAlt2 = np.degrees(get_angles_0pi(RecoAlt))
    RecoAz2 = np.degrees(get_angles_pipi(RecoAz))
    AltSource = np.degrees(get_angles_0pi(SimuAlt[0]))
    AzSource = np.degrees(get_angles_pipi(SimuAz[0]))
    return RecoAlt2, RecoAz2, AltSource, AzSource


def impact_parameter_error(RecoX, RecoY, SimuX, SimuY):
    """
    compute the error distance between simulated and reconstructed impact parameters
    Parameters
    ----------
    RecoX: 1d numpy array
    RecoY
    SimuX
    SimuY

    Returns
    -------
    1d numpy array: distances
    """
    return np.sqrt((RecoX-SimuX)**2 + (RecoY-SimuY)**2)


def RQ(x, Q=68):
    """
    Compute the value of the Qth containment radius
    Return 0 if the list is empty
    Parameters
    ----------
    x: numpy array or list

    Returns
    -------
    float
    """
    if len(x) == 0:
        return 0
    else:
        return np.percentile(x, Q)


def angular_separation_altaz(alt1, az1, alt2, az2, unit='rad'):
    """
    Compute the angular separation in radians or degrees
    between two pointing direction given with alt-az

    Parameters
    ----------
    alt1: 1d `numpy.ndarray`, altitude of the first pointing direction
    az1: 1d `numpy.ndarray` azimuth of the first pointing direction
    alt2: 1d `numpy.ndarray`, altitude of the second pointing direction
    az2: 1d `numpy.ndarray`, azimuth of the second pointing direction
    unit: 'deg' or 'rad'

    Returns
    -------
    1d `numpy.ndarray` or float, angular separation
    """
    if unit=='deg':
        alt1 = np.radians(alt1)
        az1 = np.radians(az1)
        alt2 = np.radians(alt2)
        az2 = np.radians(az2)

    cosdelta = np.cos(alt1) * np.cos(alt2) * np.cos(az1-az2) \
                + np.sin(alt1) * np.sin(alt2)
    cosdelta[cosdelta > 1] = 1.
    cosdelta[cosdelta < -1] = -1.

    ang_sep = np.degrees(np.arccos(cosdelta)) if unit=='deg' \
                else np.arccos(cosdelta)

    return ang_sep


def logbin_mean(E_bin):
    """
    Function that gives back the mean of each bin in logscale

    Parameters
    ----------
    E_bin: `numpy.ndarray`

    Returns
    -------
    `numpy.ndarray`
    """
    return 10 ** ((np.log10(E_bin[:-1]) + np.log10(E_bin[1:])) / 2.)


def impact_resolution(RecoX, RecoY, SimuX, SimuY, Q=68, conf=1.645):
    """
    Compute the shower impact parameter resolution as the Qth (68 as standard) containment radius of the square distance
    to the simulated one with the lower and upper limits corresponding to the required confidence level (1.645 for 95%)

    Parameters
    ----------
    RecoX: `numpy.ndarray`
    RecoY: `numpy.ndarray`
    SimuX: `numpy.ndarray`
    SimuY: `numpy.ndarray`
    conf: `float`

    Returns
    -------
    `numpy.array` - [impact_resolution, lower_limit, upper_limit]
    """
    d2 = impact_parameter_error(RecoX, RecoY, SimuX, SimuY)**2
    return np.sqrt(np.append(RQ(d2, Q), percentile_confidence_interval(d2, percentile=Q, conf=conf)))


def impact_resolution_per_energy(RecoX, RecoY, SimuX, SimuY, Energy, Q=68, conf=1.645):
    """
    Plot the angular resolution as a function of the event simulated energy

    Parameters
    ----------
    RecoX: `numpy.ndarray`
    RecoY: `numpy.ndarray`
    SimuX: `numpy.ndarray`
    SimuY: `numpy.ndarray`
    Energy: `numpy.ndarray`

    Returns
    -------
    (E, RES) : (1d numpy array, 1d numpy array) = Energies, Resolution
    """
    assert len(RecoX) == len(Energy)
    assert len(Energy) > 0, "Empty arrays"

    irf = irf_cta()

    E_bin = irf.E_bin
    RES = []

    for i, e in enumerate(E_bin[:-1]):
        mask = (Energy > E_bin[i]) & (Energy <= E_bin[i+1])
        RES.append(impact_resolution(RecoX[mask], RecoY[mask], SimuX[mask], SimuY[mask], Q=Q, conf=conf))

    return E_bin, np.array(RES)


def percentile_confidence_interval(x, percentile=68, conf=1.645):
    """
    Return the confidence interval for the qth percentile of X
    conf=1.96 corresponds to a 95% confidence interval for a normal distribution
    One can obtain another confidence coefficient thanks to `scipy.stats.norm.ppf`

    REF:
    http://people.stat.sfu.ca/~cschwarz/Stat-650/Notes/PDF/ChapterPercentiles.pdf
    S. Chakraborti and J. Li, Confidence Interval Estimation of a Normal Percentile, doi:10.1198/000313007X244457

    Parameters
    ----------
    x: `numpy.ndarray`
    percentile: `float` - percentile (between 0 and 100)
    conf: `float` - confidence

    Returns
    -------

    """
    sorted_x = np.sort(x)
    if len(x)==0:
        return (0, 0)
    q = percentile / 100.
    j = np.max([0, np.int(len(x) * q - conf * np.sqrt(len(x) * q * (1 - q)))])
    k = np.min([np.int(len(x) * q + conf * np.sqrt(len(x) * q * (1 - q))), len(x) - 1])
    return sorted_x[j], sorted_x[k]


def power_law_integrated_distribution(xmin, xmax, total_number_events, spectral_index, bins):
    """
    For each bin, return the expected number of events for a power-law distribution.
    bins: `numpy.ndarray`, e.g. `np.logspace(np.log10(emin), np.logspace(xmax))`
    
    Parameters
    ----------
    xmin: `float`, min of the simulated power-law
    xmax: `float`, max of the simulated power-law
    total_number_events: `int`
    spectral_index: `float`
    bins: `numpy.ndarray`
    
    Returns
    -------
    y: `numpy.ndarray`, len(y) = len(bins) - 1
    """
    if spectral_index == -1:
        y0 = total_number_events / np.log(xmax / xmin)
        y = y0 * np.log(bins[1:] / bins[:-1])
    else:
        y0 = total_number_events / (xmax ** (spectral_index + 1) - xmin ** (spectral_index + 1)) * (spectral_index + 1)
        y = y0 * (bins[1:] ** (spectral_index + 1) - bins[:-1] ** (spectral_index + 1)) / (spectral_index + 1)
    return y


def effective_area_per_energy_power_law(emin, emax, total_number_events, spectral_index, RecoE, simuArea):
    """
    Compute the effective area per energy bins from a list of simulated energies and reconstructed energies

    Parameters
    ----------
    SimuE: 1d numpy array
    RecoE: 1d numpy array
    simuArea: float - area on which events are simulated

    Returns
    -------
    (E, Seff) : (1d numpy array, 1d numpy array)
    """

    irf = irf_cta()
    bins = irf.E_bin
    simu_per_bin = power_law_integrated_distribution(emin, emax, total_number_events, spectral_index, bins)
    count_R, bin_R = np.histogram(RecoE, bins=bins)

    np.seterr(divide='ignore', invalid='ignore')
    return bins, np.nan_to_num(simuArea * count_R / simu_per_bin)

