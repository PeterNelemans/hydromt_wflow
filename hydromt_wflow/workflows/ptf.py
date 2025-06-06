"""PTF workflows for Wflow plugin."""

import math

import numpy as np


def kv_brakensiek(thetas, clay, sand):
    """
    Determine saturated hydraulic conductivity kv [mm/day].

    Based on:
      Brakensiek, D.L., Rawls, W.J.,and Stephenson, G.R.: Modifying scs hydrologic
      soil groups and curve numbers for range land soils, ASAE Paper no. PNR-84-203,
      St. Joseph, Michigan, USA, 1984.

    Parameters
    ----------
    thetas: float
        saturated water content [m3/m3].
    clay : float
        clay percentage [%].
    sand: float
        sand percentage [%].

    Returns
    -------
    kv : float
        saturated hydraulic conductivity [mm/day].

    """
    kv = (
        np.exp(
            19.52348 * thetas
            - 8.96847
            - 0.028212 * clay
            + (1.8107 * 10**-4) * sand**2
            - (9.4125 * 10**-3) * clay**2
            - 8.395215 * thetas**2
            + 0.077718 * sand * thetas
            - 0.00298 * sand**2 * thetas**2
            - 0.019492 * clay**2 * thetas**2
            + (1.73 * 10**-5) * sand**2 * clay
            + 0.02733 * clay**2 * thetas
            + 0.001434 * sand**2 * thetas
            - (3.5 * 10**-6) * clay**2 * sand
        )
        * (2.78 * 10**-6)
        * 1000
        * 3600
        * 24
    )

    return kv


def kv_cosby(sand, clay):
    """
    Determine saturated hydraulic conductivity kv [mm/day].

    based on:
      Cosby, B.J., Hornberger, G.M., Clapp, R.B., Ginn, T.R., 1984.
      A statistical exploration of the relationship of soil moisture characteristics to
      the physical properties of soils. Water Resour. Res. 20(6) 682-690.

    Parameters
    ----------
    sand: float
        sand percentage [%].
    clay : float
        clay percentage [%].

    Returns
    -------
    kv : float
        saturated hydraulic conductivity [mm/day].

    """
    kv = 60.96 * 10.0 ** (-0.6 + 0.0126 * sand - 0.0064 * clay) * 10.0

    return kv


def pore_size_index_brakensiek(sand, thetas, clay):
    """
    Determine Brooks-Corey pore size distribution index [-].

    Based on:
      Rawls,W. J., and Brakensiek, D. L.: Estimation of SoilWater Retention and
      Hydraulic Properties, In H. J. Morel-Seytoux (Ed.),
      Unsaturated flow in hydrologic modelling - Theory and practice, NATO ASI Series 9,
      275–300, Dordrecht, The Netherlands: Kluwer Academic Publishing, 1989.

    Parameters
    ----------
    sand: float
        sand percentage [%].
    thetas : float
        saturated water content [m3/m3].
    clay: float
        clay percentage [%].

    Returns
    -------
    poresizeindex : float
        pore size distribution index [-].

    """
    poresizeindex = np.exp(
        -0.7842831
        + 0.0177544 * sand
        - 1.062498 * thetas
        - (5.304 * 10**-5) * (sand**2)
        - 0.00273493 * (clay**2)
        + 1.11134946 * (thetas**2)
        - 0.03088295 * sand * thetas
        + (2.6587 * 10**-4) * (sand**2) * (thetas**2)
        - 0.00610522 * (clay**2) * (thetas**2)
        - (2.35 * 10**-6) * (sand**2) * clay
        + 0.00798746 * (clay**2) * thetas
        - 0.00674491 * (thetas**2) * clay
    )

    return poresizeindex


def thetas_toth(ph, bd, clay, silt):
    """
    Determine saturated water content [m3/m3].

    Based on:
      Tóth, B., Weynants, M., Nemes, A., Makó, A., Bilas, G., and Tóth, G.:
      New generation of hydraulic pedotransfer functions for Europe, Eur. J.
      Soil Sci., 66, 226–238. doi: 10.1111/ejss.121921211, 2015.

    Parameters
    ----------
    ph: float
        pH [-].
    bd : float
        bulk density [g /cm3].
    sand: float
        sand percentage [%].
    silt: float
        silt percentage [%].

    Returns
    -------
    thetas : float
        saturated water content [cm3/cm3].

    """
    thetas = (
        0.5653
        - 0.07918 * bd**2
        + 0.001671 * ph**2
        + 0.0005438 * clay
        + 0.001065 * silt
        + 0.06836
        - 0.00001382 * clay * ph**2
        - 0.00001270 * silt * clay
        - 0.0004784 * bd**2 * ph**2
        - 0.0002836 * silt * bd**2
        + 0.0004158 * clay * bd**2
        - 0.01686 * bd**2
        - 0.0003541 * silt
        - 0.0003152 * ph**2
    )

    return thetas


def thetar_rawls_brakensiek(sand, clay, thetas):
    """
    Determine residual water content [m3/m3].

    Based on:
      Rawls,W. J., and Brakensiek, D. L.: Estimation of SoilWater Retention and
      Hydraulic Properties, In H. J. Morel-Seytoux (Ed.),
      Unsaturated flow in hydrologic modelling - Theory and practice, NATO ASI Series 9,
      275–300, Dordrecht, The Netherlands: Kluwer Academic Publishing, 1989.

    Parameters
    ----------
    sand : float
        sand percentage [%].
    clay: float
        clay percentage [%].
    thetas: float
        saturated water content [m3/m3].

    Returns
    -------
    thetar : float
        residual water content [m3/m3].

    """
    thetar = (
        -0.0182482
        + 8.7269 * 10**-4 * sand
        + 0.00513488 * clay
        + 0.02939286 * thetas
        - 1.5395 * 10**-4 * clay**2
        - 1.0827 * 10**-3 * sand * thetas
        - 1.8233 * 10**-4 * clay**2 * thetas**2
        + 3.0703 * 10**-4 * clay**2 * thetas
        - 2.3584 * 10**-3 * thetas**2 * clay
    )

    return thetar


def soil_texture_usda(clay, silt):
    """
    Determine USDA soil texture.

    Parameters
    ----------
    clay: float
        sand percentage [%].
    silt: float
        silt percentage [%].

    Returns
    -------
    soil texture : int
        based on integer mapping following Ballabio et al. 2016 \
(https://doi.org/10.1016/j.geoderma.2015.07.006) for \
European topsoil physical properties.
        Value	NAME
        1	Clay
        2	Silty Clay
        3	Silty Clay-Loam
        4	Sandy Clay
        5	Sandy Clay-Loam
        6	Clay-Loam
        7	Silt
        8	Silt-Loam
        9	Loam
        10	Sand
        11	Loamy Sand
        12	Sandy Loam


    """
    sand = 100 - (clay + silt)

    soil_texture = np.where(
        np.logical_and(clay >= 40.0, sand >= 20.0, sand <= 45),
        1,  # clay
        np.where(
            np.logical_and(clay >= 27.0, sand >= 20.0, sand <= 45),
            6,  # clay loam
            np.where(
                np.logical_and(silt <= 40.0, sand <= 20.0),
                1,  # clay
                np.where(
                    np.logical_and(silt > 40.0, clay >= 40.0),
                    2,  # silty clay
                    np.where(
                        np.logical_and(clay >= 35.0, sand >= 45.0),
                        4,  # sandy clay
                        np.where(
                            np.logical_and(clay >= 27.0, sand < 20.0),
                            3,  # silty clay loam
                            np.where(
                                np.logical_and(clay <= 10.0, silt >= 80.0),
                                7,  # silt
                                np.where(
                                    (silt >= 50.0),
                                    8,  # silt loam
                                    np.where(
                                        np.logical_and(
                                            clay >= 7.0, sand <= 52.0, silt >= 28.0
                                        ),
                                        9,  # loam
                                        np.where(
                                            (clay >= 20.0),
                                            5,  # sandy clay loam
                                            np.where(
                                                (clay >= (sand - 70)),
                                                12,  # sandy loam
                                                np.where(
                                                    (clay >= (2 * sand - 170.0)),
                                                    11,  # loamy sand
                                                    np.where(
                                                        np.isnan(clay), np.nan, 10
                                                    ),  # sand
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )

    return soil_texture


def ErosK_texture(clay, silt):
    """
    Determine mean detachability of the soil (Morgan et al., 1998).

    Based on USDA soil texture.

    Parameters
    ----------
    clay: float
        sand percentage [%].
    silt: float
        silt percentage [%].

    Returns
    -------
    ErosK : float
        mean detachability of the soil [g/J].

    """
    sand = 100 - (clay + silt)

    erosK = np.where(
        np.logical_and(clay >= 40.0, sand >= 20.0, sand <= 45),
        2.0,  # clay
        np.where(
            np.logical_and(clay >= 27.0, sand >= 20.0, sand <= 45),
            1.7,  # clay loam
            np.where(
                np.logical_and(silt <= 40.0, sand <= 20.0),
                2.0,  # clay
                np.where(
                    np.logical_and(silt > 40.0, clay >= 40.0),
                    1.6,  # silty clay
                    np.where(
                        np.logical_and(clay >= 35.0, sand >= 45.0),
                        1.9,  # sandy clay
                        np.where(
                            np.logical_and(clay >= 27.0, sand < 20.0),
                            1.6,  # silty clay loam
                            np.where(
                                np.logical_and(clay <= 10.0, silt >= 80.0),
                                1.2,  # silt
                                np.where(
                                    (silt >= 50.0),
                                    1.5,  # silt loam
                                    np.where(
                                        np.logical_and(
                                            clay >= 7.0, sand <= 52.0, silt >= 28.0
                                        ),
                                        2.0,  # loam
                                        np.where(
                                            (clay >= 20.0),
                                            2.1,  # sandy clay loam
                                            np.where(
                                                (clay >= (sand - 70)),
                                                2.6,  # sandy loam
                                                np.where(
                                                    (clay >= (2 * sand - 170.0)),
                                                    3.0,  # loamy sand
                                                    np.where(
                                                        np.isnan(clay), np.nan, 1.9
                                                    ),  # sand
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )

    return erosK


def UsleK_Renard(clay, silt):
    """
    Determine USLE K factor based on Renard.

    Parameters
    ----------
    clay: float
        sand percentage [%].
    silt: float
        silt percentage [%].

    Returns
    -------
    usleK : float
        soil erodibility factor from the USLE equation [-].

    """
    sand = 100 - (clay + silt)

    Dg = np.exp(
        0.01
        * (clay * math.log(0.001) + silt * math.log(0.025) + sand * math.log(0.999))
    )
    usleK = 0.0034 + 0.0405 * np.exp(-0.5 * ((np.log(Dg) + 1.659) / 0.7101) ** 2)

    return usleK


def UsleK_EPIC(clay, silt, oc):
    """
    Determine USLE K factor based on EPIC formula.

    Parameters
    ----------
    clay: float
        sand percentage [%].
    silt: float
        silt percentage [%].
    oc : float
        organic carbon [%].

    Returns
    -------
    usleK : float
        soil erodibility factor from the USLE equation [-].

    """
    sand = 100 - (clay + silt)
    SN = 1 - (sand) / 100

    usleK = (
        (0.2 + 0.3 * np.exp(-0.0256 * sand * (1 - silt / 100)))
        * (silt / (clay + silt)) ** 0.3
        * (1 - (0.25 * oc) / (oc + np.exp(3.72 - 2.95 * oc)))
        * (1 - (0.7 * SN) / (SN + np.exp(22.9 * SN - 5.31)))
    )
    # Conversion to SI units
    usleK = (1 / 7.594) * usleK

    return usleK


def mean_diameter_soil(clay, silt):
    """
    Determine mean diameter of the soil using Fooladmand et al. (2006).

    Parameters
    ----------
    clay: float
        clay percentage [%].
    silt: float
        silt percentage [%].

    Returns
    -------
    d50 : float
        mean diameter of the soil [mm].
    """
    sand = 100 - (clay + silt)
    sand999 = sand * ((999 - 25) / (1000 - 25))

    vd50 = np.log((1 / (0.01 * (clay + silt)) - 1) / (1 / (0.01 * clay) - 1))
    wd50 = np.log((1 / (0.01 * (clay + silt + sand999)) - 1) / (1 / (0.01 * clay) - 1))
    ad50 = 1 / np.log((25 - 1) / (999 - 1))
    bd50 = ad50 / np.log((25 - 1) / 1)
    cd50 = ad50 * np.log(vd50 / wd50)
    ud50 = (-vd50) ** (1 - bd50) / ((-wd50) ** (-bd50))
    d50 = 1 + (-1 / ud50 * np.log(1 / (1 / (0.01 * clay) - 1))) ** (1 / cd50)  # [um]
    d50 = d50 / 1000  # [mm]

    return d50


def air_entry_pressure(clay, silt, porosity):
    """
    Determine air entry pressure for soils with 5-60% clay and 5-70% sand.

    Based on:
      Rawls, W.J., and D.L. Brakensiek. 1985. Prediction of soil water
      properties for hydrologic modeling. p. 293-299. In E.B. Jones and
      T.J.Ward (ed.) Proc. Symp.Watershed Management in the Eighties,
      Denver, CO. 30 Apr.-1 May 1985. Am. Soc. Civil Eng., New York mapping

    Parameters
    ----------
    clay: float
        clay percentage [%].
    silt: float
        silt percentage [%].
    porosity: float
        porosity of the soil [-].

    Returns
    -------
    air_entry_pressure : float
        based on equation from Rawls & Brakensiek (1985).

    """
    sand = 100 - (clay + silt)

    air_entry_pressure = np.where(
        np.logical_and(
            np.logical_and(clay > 5.0, clay < 60), np.logical_and(sand > 5, sand < 70)
        ),
        -np.exp(
            5.3396738
            + 0.1845038 * clay
            - 2.48394546 * porosity
            - 0.00213853 * (clay**2)
            - 0.04356349 * sand * porosity
            - 0.61745089 * clay * porosity
            + 0.00143598 * (sand**2) * (porosity**2)
            - 0.00855375 * (clay**2) * (porosity**2)
            - 0.00001282 * (sand**2) * clay
            + 0.00895359 * (clay**2) * porosity
            - 0.00072472 * (sand**2) * porosity
            + 0.0000054 * (clay**2) * sand
            + 0.50028060 * (porosity**2) * clay
        ),
        np.nan,
    )

    return air_entry_pressure
