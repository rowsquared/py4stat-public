import pandas as pd
import numpy as np
from typing import Optional, List, Literal
from datetime import datetime, timedelta
import random


def get_provinces() -> pd.DataFrame:
    """Return Datania province reference data."""
    data = {
        'province_code': ['NTH', 'STH', 'EST', 'WST', 'CTR', 'LKS'],
        'province_name': ['Northern Province', 'Southern Province', 'Eastern Province',
                          'Western Province', 'Central Province', 'Lakeside Province'],
        'capital': ['Polaris', 'Median City', 'Outlier Bay', 'Deviation', 'Numerica', 'Port Sample'],
        'population': [2_100_000, 3_800_000, 2_500_000, 1_900_000, 5_200_000, 3_000_000],
        'character': ['Rural, agricultural, mining', 'Industrial, urban',
                      'Coastal, fishing, tourism', 'Semi-arid, livestock',
                      'Capital region, services, government', 'Agriculture, lake fishing']
    }
    return pd.DataFrame(data)


def get_districts() -> pd.DataFrame:
    """Return Datania district reference data."""
    districts = {
        'CTR': ['Numerica Urban', 'Numerica Peri-Urban', 'Variance District', 'Range District'],
        'NTH': ['Polaris District', 'Sigma District', 'Correlation Hills', 'Regression Valley'],
        'STH': ['Median Urban', 'Mode District', 'Frequency Plains', 'Distribution District'],
        'EST': ['Outlier Coastal', 'Skewness District', 'Kurtosis Bay', 'Percentile District'],
        'WST': ['Deviation District', 'Standard District', 'Error Margin', 'Confidence District'],
        'LKS': ['Port Sample District', 'Parameter District', 'Estimate District', 'Interval District']
    }
    rows = []
    for province_code, district_list in districts.items():
        for district in district_list:
            rows.append({'province_code': province_code, 'district_name': district})
    return pd.DataFrame(rows)

def get_cities() -> pd.DataFrame:
    """Return Datania major cities reference data."""
    data = {
        'city': ['Numerica', 'Median City', 'Outlier Bay', 'Polaris', 'Deviation',
                 'Port Sample', 'Variance Town', 'Mode Village', 'Quartile Heights', 'Sigma Falls'],
        'province_code': ['CTR', 'STH', 'EST', 'NTH', 'WST', 'LKS', 'CTR', 'STH', 'EST', 'NTH'],
        'population': [1_800_000, 950_000, 420_000, 280_000, 210_000,
                       350_000, 180_000, 95_000, 75_000, 60_000],
        'notes': ['Capital city, DNSO headquarters', 'Industrial hub', 'Major port city',
                  'Mining center', 'Agricultural market town', 'Fishing and agriculture',
                  'University town', 'Manufacturing', 'Tourism, coastal', 'Hydroelectric, rural']
    }
    return pd.DataFrame(data)


def generate_census_data(
        n_persons: int = 1000,
        seed: int = 42
) -> pd.DataFrame:
    """
    Generate synthetic population census data for Datania.

    Parameters:
        n_persons: Number of individual records to generate
        seed: Random seed for reproducibility

    Returns:
        DataFrame with census microdata
    """
    np.random.seed(seed)
    random.seed(seed)

    provinces = get_provinces()
    districts = get_districts()

    # Province weights based on population
    province_weights = provinces['population'] / provinces['population'].sum()

    # Urbanization rates by province
    urban_rates = {
        'CTR': 0.75, 'STH': 0.60, 'EST': 0.45,
        'WST': 0.25, 'NTH': 0.30, 'LKS': 0.35
    }

    records = []
    hh_id = 1000
    person_in_hh = 0
    hh_size = np.random.poisson(4.5) + 1  # Average household size ~5

    for i in range(n_persons):
        # Assign to household
        if person_in_hh >= hh_size:
            hh_id += 1
            person_in_hh = 0
            hh_size = max(1, np.random.poisson(4.5) + 1)

        # Province (weighted by population)
        province = np.random.choice(provinces['province_code'], p=province_weights)

        # District within province
        prov_districts = districts[districts['province_code'] == province]['district_name'].tolist()
        district = random.choice(prov_districts)

        # Urban/Rural
        urban_rural = 'Urban' if np.random.random() < urban_rates[province] else 'Rural'

        # EA code (enumeration area)
        ea_code = f"{province}-{district[:3].upper()}-{np.random.randint(1, 100):03d}"

        # Age: Young population pyramid
        # Use exponential-like distribution for developing country demographics
        age = int(np.random.exponential(22))
        age = min(age, 95)  # Cap at 95

        # Sex
        sex = 'Female' if np.random.random() < 0.51 else 'Male'

        # Education (correlated with age and urban/rural)
        if age < 6:
            education = 'None (below school age)'
        elif age < 15:
            education = np.random.choice(
                ['None', 'Primary incomplete', 'Primary complete'],
                p=[0.1, 0.6, 0.3]
            )
        else:
            # Adults - education depends on urban/rural
            if urban_rural == 'Urban':
                education = np.random.choice(
                    ['None', 'Primary incomplete', 'Primary complete',
                     'Secondary incomplete', 'Secondary complete', 'Tertiary'],
                    p=[0.08, 0.12, 0.25, 0.20, 0.25, 0.10]
                )
            else:
                education = np.random.choice(
                    ['None', 'Primary incomplete', 'Primary complete',
                     'Secondary incomplete', 'Secondary complete', 'Tertiary'],
                    p=[0.15, 0.25, 0.30, 0.15, 0.12, 0.03]
                )

        # Marital status (age-dependent)
        if age < 15:
            marital = 'Never married'
        elif age < 25:
            marital = np.random.choice(
                ['Never married', 'Married', 'Cohabiting'],
                p=[0.65, 0.25, 0.10]
            )
        elif age < 50:
            marital = np.random.choice(
                ['Never married', 'Married', 'Cohabiting', 'Divorced/Separated', 'Widowed'],
                p=[0.15, 0.60, 0.10, 0.10, 0.05]
            )
        else:
            marital = np.random.choice(
                ['Never married', 'Married', 'Divorced/Separated', 'Widowed'],
                p=[0.05, 0.50, 0.15, 0.30]
            )

        # Relationship to head
        if person_in_hh == 0:
            relationship = 'Head'
        elif person_in_hh == 1 and age >= 15:
            relationship = 'Spouse'
        else:
            relationship = np.random.choice(
                ['Son/Daughter', 'Grandchild', 'Parent', 'Other relative', 'Non-relative'],
                p=[0.50, 0.20, 0.10, 0.15, 0.05]
            )

        records.append({
            'person_id': f"PHC2020-{i + 1:07d}",
            'hh_id': f"HH-{hh_id:06d}",
            'province': province,
            'district': district,
            'urban_rural': urban_rural,
            'ea_code': ea_code,
            'age': age,
            'sex': sex,
            'education_level': education,
            'marital_status': marital,
            'relationship_to_head': relationship
        })

        person_in_hh += 1

    return pd.DataFrame(records)


def generate_household_survey(
        n_households: int = 500,
        survey_year: int = 2025,
        seed: int = 42
) -> pd.DataFrame:
    """
    Generate synthetic household survey data for Datania (DHHS-style).

    Parameters:
        n_households: Number of households to generate
        survey_year: Year of the survey
        seed: Random seed for reproducibility

    Returns:
        DataFrame with household-level survey data
    """
    np.random.seed(seed)
    random.seed(seed)

    provinces = get_provinces()
    districts = get_districts()

    province_weights = provinces['population'] / provinces['population'].sum()

    urban_rates = {
        'CTR': 0.75, 'STH': 0.60, 'EST': 0.45,
        'WST': 0.25, 'NTH': 0.30, 'LKS': 0.35
    }

    # Base income by province (in DKW - Datanian Kwacha)
    base_income = {
        'CTR': 45000, 'STH': 38000, 'EST': 32000,
        'WST': 22000, 'NTH': 25000, 'LKS': 28000
    }

    records = []

    for i in range(n_households):
        province = np.random.choice(provinces['province_code'], p=province_weights)
        prov_districts = districts[districts['province_code'] == province]['district_name'].tolist()
        district = random.choice(prov_districts)
        urban_rural = 'Urban' if np.random.random() < urban_rates[province] else 'Rural'

        # Household composition
        hh_size = max(1, int(np.random.poisson(4.2) + 1))
        n_children = min(hh_size - 1, max(0, int(np.random.poisson(1.8))))
        n_elderly = min(hh_size - n_children - 1, max(0, int(np.random.exponential(0.4))))
        n_working_age = hh_size - n_children - n_elderly

        # Income (log-normal, urban premium)
        urban_premium = 1.4 if urban_rural == 'Urban' else 1.0
        base = base_income[province] * urban_premium
        monthly_income = max(5000, int(np.random.lognormal(np.log(base), 0.6)))

        # Expenditure (correlated with income)
        propensity = np.random.uniform(0.75, 0.95)
        monthly_expenditure = int(monthly_income * propensity * np.random.uniform(0.9, 1.1))

        # Assets (probability increases with income and urban status)
        income_factor = min(monthly_income / 50000, 2)
        urban_factor = 1.3 if urban_rural == 'Urban' else 1.0

        has_electricity = np.random.random() < (0.3 + 0.4 * urban_factor * income_factor)
        has_improved_water = np.random.random() < (0.4 + 0.3 * urban_factor * income_factor)
        has_improved_sanitation = np.random.random() < (0.25 + 0.35 * urban_factor * income_factor)
        owns_radio = np.random.random() < 0.70
        owns_tv = np.random.random() < (0.15 + 0.35 * urban_factor * income_factor)
        owns_mobile = np.random.random() < (0.50 + 0.30 * income_factor)
        owns_refrigerator = np.random.random() < (0.05 + 0.25 * urban_factor * income_factor)
        owns_vehicle = np.random.random() < (0.02 + 0.10 * income_factor)

        # Dwelling type
        if urban_rural == 'Urban':
            dwelling = np.random.choice(
                ['Detached house', 'Semi-detached', 'Flat/Apartment', 'Single room', 'Informal'],
                p=[0.25, 0.20, 0.15, 0.25, 0.15]
            )
        else:
            dwelling = np.random.choice(
                ['Traditional hut', 'Detached house', 'Semi-detached', 'Single room'],
                p=[0.35, 0.40, 0.15, 0.10]
            )

        # Survey weight (inverse probability of selection)
        # Urban areas over-sampled, so rural gets higher weight
        base_weight = 1.0
        if urban_rural == 'Rural':
            base_weight *= 1.5
        # Small provinces get higher weight
        prov_pop = provinces[provinces['province_code'] == province]['population'].values[0]
        base_weight *= (provinces['population'].mean() / prov_pop)
        survey_weight = round(base_weight * np.random.uniform(0.9, 1.1), 2)

        records.append({
            'hh_id': f"DHHS{survey_year}-{i + 1:05d}",
            'province': province,
            'district': district,
            'urban_rural': urban_rural,
            'hh_size': hh_size,
            'n_children': n_children,
            'n_working_age': n_working_age,
            'n_elderly': n_elderly,
            'monthly_income': monthly_income,
            'monthly_expenditure': monthly_expenditure,
            'has_electricity': has_electricity,
            'has_improved_water': has_improved_water,
            'has_improved_sanitation': has_improved_sanitation,
            'owns_radio': owns_radio,
            'owns_tv': owns_tv,
            'owns_mobile': owns_mobile,
            'owns_refrigerator': owns_refrigerator,
            'owns_vehicle': owns_vehicle,
            'dwelling_type': dwelling,
            'survey_weight': survey_weight
        })

    return pd.DataFrame(records)


def generate_labour_force_survey(
        n_persons: int = 1000,
        year: int = 2026,
        quarter: int = 1,
        seed: int = 42
) -> pd.DataFrame:
    """
    Generate synthetic Quarterly Labour Force Survey data for Datania.

    Parameters:
        n_persons: Number of working-age individuals (15+)
        year: Survey year
        quarter: Survey quarter (1-4)
        seed: Random seed for reproducibility

    Returns:
        DataFrame with QLFS microdata
    """
    np.random.seed(seed)
    random.seed(seed)

    provinces = get_provinces()
    districts = get_districts()

    province_weights = provinces['population'] / provinces['population'].sum()

    urban_rates = {
        'CTR': 0.75, 'STH': 0.60, 'EST': 0.45,
        'WST': 0.25, 'NTH': 0.30, 'LKS': 0.35
    }

    # ISCO-08 occupation codes (simplified)
    occupations = [
        ('1', 'Managers'),
        ('2', 'Professionals'),
        ('3', 'Technicians and associate professionals'),
        ('4', 'Clerical support workers'),
        ('5', 'Service and sales workers'),
        ('6', 'Skilled agricultural workers'),
        ('7', 'Craft and related trades workers'),
        ('8', 'Plant and machine operators'),
        ('9', 'Elementary occupations')
    ]

    # ISIC industry codes (simplified)
    industries = [
        ('A', 'Agriculture, forestry and fishing'),
        ('B', 'Mining and quarrying'),
        ('C', 'Manufacturing'),
        ('D', 'Electricity, gas, water supply'),
        ('F', 'Construction'),
        ('G', 'Wholesale and retail trade'),
        ('H', 'Transportation and storage'),
        ('I', 'Accommodation and food service'),
        ('J', 'Information and communication'),
        ('K', 'Financial and insurance'),
        ('M', 'Professional services'),
        ('O', 'Public administration'),
        ('P', 'Education'),
        ('Q', 'Health and social work'),
        ('S', 'Other services')
    ]

    # Base income by occupation (DKW)
    occupation_income = {
        '1': 85000, '2': 65000, '3': 48000, '4': 32000, '5': 25000,
        '6': 18000, '7': 28000, '8': 30000, '9': 15000
    }

    records = []
    hh_id = 5000

    for i in range(n_persons):
        # Cycle household IDs
        if i % 4 == 0:
            hh_id += 1

        province = np.random.choice(provinces['province_code'], p=province_weights)
        prov_districts = districts[districts['province_code'] == province]['district_name'].tolist()
        district = random.choice(prov_districts)
        urban_rural = 'Urban' if np.random.random() < urban_rates[province] else 'Rural'

        # Age (working age population 15-64, with some 65+)
        age = int(np.random.triangular(15, 28, 70))
        age = max(15, min(age, 75))

        sex = 'Female' if np.random.random() < 0.52 else 'Male'

        # Education
        education = np.random.choice(
            ['None', 'Primary', 'Secondary', 'Tertiary'],
            p=[0.12, 0.35, 0.40, 0.13]
        )

        # Employment status (depends on age, education, urban/rural)
        if age >= 65:
            employed_prob = 0.25
        elif education == 'Tertiary':
            employed_prob = 0.75
        elif urban_rural == 'Urban':
            employed_prob = 0.58
        else:
            employed_prob = 0.65  # Higher in rural due to agriculture

        # Determine employment status
        rand = np.random.random()
        if rand < employed_prob:
            employment_status = 'Employed'
        elif rand < employed_prob + 0.15:
            employment_status = 'Unemployed'
        else:
            employment_status = 'Not in labour force'

        # Initialize work-related fields
        occupation_code = None
        occupation_desc = None
        industry_code = None
        industry_desc = None
        sector = None
        hours_worked = None
        monthly_income = None
        is_informal = None
        seeking_work = False

        if employment_status == 'Employed':
            # Assign occupation based on education and urban/rural
            if education == 'Tertiary':
                occ_weights = [0.15, 0.30, 0.20, 0.15, 0.10, 0.02, 0.03, 0.03, 0.02]
            elif education == 'Secondary':
                occ_weights = [0.05, 0.08, 0.12, 0.15, 0.25, 0.08, 0.12, 0.08, 0.07]
            elif urban_rural == 'Rural':
                occ_weights = [0.02, 0.02, 0.03, 0.03, 0.10, 0.45, 0.10, 0.05, 0.20]
            else:
                occ_weights = [0.03, 0.05, 0.08, 0.10, 0.30, 0.05, 0.15, 0.10, 0.14]

            occ_idx = np.random.choice(len(occupations), p=occ_weights)
            occupation_code, occupation_desc = occupations[occ_idx]

            # Industry based on occupation and province character
            if occupation_code == '6':  # Agricultural workers
                ind_idx = 0  # Agriculture
            elif province == 'NTH' and np.random.random() < 0.3:
                ind_idx = 1  # Mining in Northern
            elif province == 'STH' and np.random.random() < 0.3:
                ind_idx = 2  # Manufacturing in Southern
            else:
                if urban_rural == 'Urban':
                    ind_weights = [0.05, 0.02, 0.12, 0.03, 0.08, 0.20, 0.08, 0.10, 0.05, 0.05, 0.05, 0.05, 0.06, 0.04,
                                   0.02]
                else:
                    ind_weights = [0.40, 0.05, 0.08, 0.02, 0.05, 0.15, 0.05, 0.05, 0.02, 0.02, 0.02, 0.03, 0.03, 0.02,
                                   0.01]
                ind_idx = np.random.choice(len(industries), p=ind_weights)

            industry_code, industry_desc = industries[ind_idx]

            # Sector
            if industry_code in ['O', 'P', 'Q']:
                sector = 'Public'
            else:
                sector = 'Private'

            # Hours worked (normal distribution around 40)
            hours_worked = max(5, min(80, int(np.random.normal(42, 12))))

            # Income
            base = occupation_income[occupation_code]
            urban_mult = 1.25 if urban_rural == 'Urban' else 1.0
            sector_mult = 1.15 if sector == 'Public' else 1.0
            monthly_income = max(8000, int(np.random.lognormal(np.log(base * urban_mult * sector_mult), 0.4)))

            # Informality (higher in rural, agriculture, elementary occupations)
            informal_prob = 0.15
            if urban_rural == 'Rural':
                informal_prob += 0.25
            if industry_code == 'A':
                informal_prob += 0.30
            if occupation_code == '9':
                informal_prob += 0.25
            is_informal = np.random.random() < min(informal_prob, 0.85)

        elif employment_status == 'Unemployed':
            seeking_work = True
        else:
            seeking_work = np.random.random() < 0.1  # Some discouraged workers

        # Survey weight
        prov_pop = provinces[provinces['province_code'] == province]['population'].values[0]
        base_weight = provinces['population'].mean() / prov_pop
        if urban_rural == 'Rural':
            base_weight *= 1.4
        survey_weight = round(base_weight * np.random.uniform(0.9, 1.1), 2)

        records.append({
            'person_id': f"QLFS{year}Q{quarter}-{i + 1:06d}",
            'hh_id': f"HH-{hh_id:06d}",
            'province': province,
            'district': district,
            'urban_rural': urban_rural,
            'age': age,
            'sex': sex,
            'education_level': education,
            'employment_status': employment_status,
            'occupation_code': occupation_code,
            'occupation_desc': occupation_desc,
            'industry_code': industry_code,
            'industry_desc': industry_desc,
            'sector': sector,
            'hours_worked': hours_worked,
            'monthly_income': monthly_income,
            'is_informal': is_informal,
            'seeking_work': seeking_work,
            'quarter': quarter,
            'year': year,
            'survey_weight': survey_weight
        })

    return pd.DataFrame(records)


def generate_business_register(
        n_businesses: int = 500,
        reference_year: int = 2025,
        seed: int = 42
) -> pd.DataFrame:
    """
    Generate synthetic business register data for Datania (DAES-style).

    Parameters:
        n_businesses: Number of business establishments
        reference_year: Reference year for the register
        seed: Random seed for reproducibility

    Returns:
        DataFrame with business register data
    """
    np.random.seed(seed)
    random.seed(seed)

    provinces = get_provinces()
    districts = get_districts()
    cities = get_cities()

    # Business concentration in urban/industrial areas
    province_weights = np.array([0.10, 0.25, 0.15, 0.08, 0.30, 0.12])  # Heavier in CTR, STH

    urban_rates = {
        'CTR': 0.85, 'STH': 0.75, 'EST': 0.60,
        'WST': 0.40, 'NTH': 0.45, 'LKS': 0.50
    }

    industries = [
        ('A', 'Agriculture, forestry and fishing'),
        ('C', 'Manufacturing'),
        ('F', 'Construction'),
        ('G', 'Wholesale and retail trade'),
        ('H', 'Transportation and storage'),
        ('I', 'Accommodation and food service'),
        ('J', 'Information and communication'),
        ('K', 'Financial and insurance'),
        ('M', 'Professional services'),
        ('N', 'Administrative services'),
        ('Q', 'Health and social work'),
        ('R', 'Arts and entertainment'),
        ('S', 'Other services')
    ]

    # Business name prefixes and suffixes
    prefixes = ['Datania', 'National', 'Central', 'Premier', 'Elite', 'Golden',
                'United', 'Modern', 'Quality', 'Trust', 'Pioneer', 'Excel']
    suffixes_by_industry = {
        'A': ['Farms', 'Agro', 'Agricultural', 'Growers', 'Harvest'],
        'C': ['Manufacturing', 'Industries', 'Products', 'Works', 'Factory'],
        'F': ['Construction', 'Builders', 'Engineering', 'Contractors'],
        'G': ['Trading', 'Wholesale', 'Retail', 'Stores', 'Mart', 'Shop'],
        'H': ['Transport', 'Logistics', 'Freight', 'Movers', 'Express'],
        'I': ['Hotel', 'Restaurant', 'Lodge', 'Catering', 'Foods'],
        'J': ['Tech', 'IT Solutions', 'Digital', 'Systems', 'Software'],
        'K': ['Finance', 'Insurance', 'Investments', 'Capital'],
        'M': ['Consulting', 'Advisory', 'Associates', 'Partners'],
        'N': ['Services', 'Support', 'Solutions', 'Management'],
        'Q': ['Clinic', 'Medical', 'Health', 'Care', 'Pharmacy'],
        'R': ['Entertainment', 'Media', 'Arts', 'Events'],
        'S': ['Services', 'Enterprises', 'Company', 'Group']
    }

    legal_statuses = ['Sole proprietorship', 'Partnership', 'Private limited company',
                      'Public limited company', 'Cooperative', 'Non-profit']

    # Province coordinates (approximate centers)
    province_coords = {
        'CTR': (-15.4, 28.3), 'STH': (-17.8, 25.9), 'EST': (-14.2, 35.1),
        'WST': (-16.5, 22.8), 'NTH': (-11.9, 31.2), 'LKS': (-13.5, 34.5)
    }

    records = []

    for i in range(n_businesses):
        province = np.random.choice(provinces['province_code'], p=province_weights)
        prov_districts = districts[districts['province_code'] == province]['district_name'].tolist()
        district = random.choice(prov_districts)
        urban_rural = 'Urban' if np.random.random() < urban_rates[province] else 'Rural'

        # Industry (depends on urban/rural and province)
        if urban_rural == 'Urban':
            ind_weights = [0.02, 0.08, 0.06, 0.25, 0.08, 0.15, 0.05, 0.04, 0.08, 0.06, 0.05, 0.03, 0.05]
        else:
            ind_weights = [0.25, 0.05, 0.04, 0.20, 0.05, 0.10, 0.02, 0.02, 0.03, 0.04, 0.08, 0.02, 0.10]

        ind_idx = np.random.choice(len(industries), p=ind_weights)
        industry_code, industry_desc = industries[ind_idx]

        # Business name
        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes_by_industry.get(industry_code, ['Enterprises']))
        business_name = f"{prefix} {suffix}"
        if np.random.random() < 0.3:
            business_name += " Ltd"

        # Legal status (larger companies more likely to be limited)
        legal_status = np.random.choice(
            legal_statuses,
            p=[0.45, 0.15, 0.25, 0.05, 0.05, 0.05]
        )

        # Year established (exponential decay - more recent establishments)
        years_ago = int(np.random.exponential(8))
        year_established = max(1960, reference_year - years_ago)

        # Number of employees (power law distribution - many small, few large)
        n_employees = max(1, int(np.random.pareto(1.5) * 2 + 1))
        n_employees = min(n_employees, 5000)  # Cap

        # Size class
        if n_employees <= 4:
            size_class = 'Micro'
        elif n_employees <= 19:
            size_class = 'Small'
        elif n_employees <= 99:
            size_class = 'Medium'
        else:
            size_class = 'Large'

        # Annual turnover (correlated with employees and industry)
        base_turnover = n_employees * np.random.uniform(80000, 200000)
        if industry_code in ['K', 'J']:  # Finance, IT higher margins
            base_turnover *= 1.5
        elif industry_code == 'A':  # Agriculture lower
            base_turnover *= 0.6
        annual_turnover = int(base_turnover * np.random.lognormal(0, 0.3))

        # Registration status (larger and urban more likely registered)
        reg_prob = 0.3
        if size_class in ['Medium', 'Large']:
            reg_prob = 0.95
        elif size_class == 'Small':
            reg_prob = 0.65
        if urban_rural == 'Urban':
            reg_prob += 0.15
        is_registered = np.random.random() < min(reg_prob, 0.98)
        has_tax_id = is_registered and (np.random.random() < 0.85)

        # Coordinates
        base_lat, base_lon = province_coords[province]
        latitude = round(base_lat + np.random.normal(0, 0.5), 4)
        longitude = round(base_lon + np.random.normal(0, 0.5), 4)

        records.append({
            'business_id': f"BIZ-{reference_year}-{i + 1:06d}",
            'business_name': business_name,
            'province': province,
            'district': district,
            'urban_rural': urban_rural,
            'industry_code': industry_code,
            'industry_desc': industry_desc,
            'legal_status': legal_status,
            'year_established': year_established,
            'n_employees': n_employees,
            'size_class': size_class,
            'annual_turnover': annual_turnover,
            'is_registered': is_registered,
            'has_tax_id': has_tax_id,
            'latitude': latitude,
            'longitude': longitude
        })

    return pd.DataFrame(records)


def generate_price_data(
        n_months: int = 12,
        start_year: int = 2025,
        start_month: int = 1,
        seed: int = 42
) -> pd.DataFrame:
    """
    Generate synthetic price index data for Datania (PICES-style).

    Parameters:
        n_months: Number of months of data to generate
        start_year: Starting year
        start_month: Starting month (1-12)
        seed: Random seed for reproducibility

    Returns:
        DataFrame with price observations
    """
    np.random.seed(seed)
    random.seed(seed)

    provinces = get_provinces()
    cities = get_cities()

    # Products with base prices (DKW), categories, and seasonality
    products = [
        # Food & Beverages
        ('F001', 'Maize flour (1kg)', 'Food - Cereals', 'kg', 45, 0.15),
        ('F002', 'Rice (1kg)', 'Food - Cereals', 'kg', 65, 0.10),
        ('F003', 'Bread (loaf)', 'Food - Cereals', 'loaf', 28, 0.05),
        ('F004', 'Beef (1kg)', 'Food - Meat', 'kg', 180, 0.08),
        ('F005', 'Chicken (1kg)', 'Food - Meat', 'kg', 145, 0.12),
        ('F006', 'Fish - dried (1kg)', 'Food - Fish', 'kg', 120, 0.20),
        ('F007', 'Tomatoes (1kg)', 'Food - Vegetables', 'kg', 35, 0.35),
        ('F008', 'Onions (1kg)', 'Food - Vegetables', 'kg', 25, 0.30),
        ('F009', 'Cooking oil (1L)', 'Food - Oils', 'litre', 85, 0.08),
        ('F010', 'Sugar (1kg)', 'Food - Sugar', 'kg', 55, 0.06),
        ('F011', 'Milk - fresh (1L)', 'Food - Dairy', 'litre', 42, 0.10),
        ('F012', 'Eggs (tray of 30)', 'Food - Eggs', 'tray', 95, 0.15),
        # Non-food
        ('N001', 'Petrol (1L)', 'Transport - Fuel', 'litre', 32, 0.03),
        ('N002', 'Diesel (1L)', 'Transport - Fuel', 'litre', 28, 0.03),
        ('N003', 'Electricity (unit)', 'Housing - Utilities', 'kWh', 2.5, 0.02),
        ('N004', 'Charcoal (50kg)', 'Housing - Fuel', 'bag', 180, 0.20),
        ('N005', 'Soap - bar', 'Personal Care', 'bar', 15, 0.05),
        ('N006', 'Mobile airtime (unit)', 'Communication', 'unit', 1, 0.01),
        ('N007', 'School uniform', 'Education', 'piece', 250, 0.08),
        ('N008', 'Paracetamol (pack)', 'Health', 'pack', 35, 0.04),
    ]

    # Markets (one per major city)
    markets = [
        ('MKT-NUM', 'Numerica Central Market', 'CTR'),
        ('MKT-MED', 'Median City Market', 'STH'),
        ('MKT-OUT', 'Outlier Bay Market', 'EST'),
        ('MKT-POL', 'Polaris Market', 'NTH'),
        ('MKT-DEV', 'Deviation Market', 'WST'),
        ('MKT-PRT', 'Port Sample Market', 'LKS'),
    ]

    # Province price multipliers (Numerica is baseline)
    province_price_mult = {
        'CTR': 1.00, 'STH': 0.95, 'EST': 1.05,
        'WST': 0.90, 'NTH': 0.92, 'LKS': 0.88
    }

    records = []
    obs_id = 1

    # Track prices for calculating changes
    prev_prices = {}

    for month_offset in range(n_months):
        # Calculate current year and month
        current_month = ((start_month - 1 + month_offset) % 12) + 1
        current_year = start_year + (start_month - 1 + month_offset) // 12
        date_str = f"{current_year}-{current_month:02d}-15"  # Mid-month observation

        # Seasonal factor (higher prices in lean season: Nov-Feb)
        if current_month in [11, 12, 1, 2]:
            seasonal_factor = 1.08
        elif current_month in [3, 4, 5]:
            seasonal_factor = 0.95  # Post-harvest
        else:
            seasonal_factor = 1.00

        # Inflation trend (gradual increase)
        inflation_factor = 1 + (0.005 * month_offset)  # ~6% annual inflation

        for market_code, market_name, province in markets:
            prov_mult = province_price_mult[province]

            for prod_code, prod_name, category, unit, base_price, volatility in products:
                # Calculate price
                price = base_price * prov_mult * seasonal_factor * inflation_factor

                # Add random noise based on volatility
                price *= np.random.lognormal(0, volatility)
                price = round(price, 2)

                # Get previous month price
                key = (market_code, prod_code)
                price_previous = prev_prices.get(key)

                if price_previous:
                    price_change_pct = round((price - price_previous) / price_previous * 100, 2)
                else:
                    price_change_pct = None

                # Store current price for next iteration
                prev_prices[key] = price

                records.append({
                    'observation_id': f"PICES-{obs_id:08d}",
                    'year': current_year,
                    'month': current_month,
                    'date': date_str,
                    'province': province,
                    'market': market_name,
                    'product_code': prod_code,
                    'product_name': prod_name,
                    'category': category,
                    'unit': unit,
                    'price': price,
                    'price_previous_month': price_previous,
                    'price_change_pct': price_change_pct
                })
                obs_id += 1

    return pd.DataFrame(records)


def generate_agricultural_survey(
        n_farms: int = 500,
        year: int = 2025,
        seed: int = 42
) -> pd.DataFrame:
    """
    Generate synthetic agricultural production survey data for Datania (DAPS-style).

    Parameters:
        n_farms: Number of farm/plot records
        year: Survey year
        seed: Random seed for reproducibility

    Returns:
        DataFrame with agricultural production data
    """
    np.random.seed(seed)
    random.seed(seed)

    provinces = get_provinces()
    districts = get_districts()

    # Agricultural provinces have higher weights
    province_weights = np.array([0.25, 0.10, 0.10, 0.20, 0.05, 0.30])  # NTH, WST, LKS more agricultural

    # Crops with base yields (kg/ha) and typical area
    crops = [
        ('C01', 'Maize', 2500, 1.5),
        ('C02', 'Rice', 3000, 0.8),
        ('C03', 'Cassava', 12000, 0.6),
        ('C04', 'Groundnuts', 800, 0.4),
        ('C05', 'Sorghum', 1200, 0.8),
        ('C06', 'Millet', 900, 0.5),
        ('C07', 'Sweet potatoes', 8000, 0.3),
        ('C08', 'Beans', 600, 0.3),
        ('C09', 'Tobacco', 1500, 0.4),
        ('C10', 'Cotton', 1000, 0.6),
        ('C11', 'Sunflower', 700, 0.5),
        ('C12', 'Vegetables (mixed)', 5000, 0.2),
    ]

    # Province crop preferences (based on character from Datania Reference)
    province_crop_weights = {
        'NTH': [0.25, 0.05, 0.10, 0.10, 0.15, 0.10, 0.05, 0.05, 0.05, 0.05, 0.03, 0.02],  # Mining region, diverse
        'STH': [0.30, 0.10, 0.15, 0.08, 0.05, 0.02, 0.08, 0.08, 0.05, 0.03, 0.03, 0.03],  # Industrial
        'EST': [0.20, 0.25, 0.10, 0.05, 0.05, 0.02, 0.05, 0.05, 0.02, 0.02, 0.02, 0.17],  # Coastal, rice
        'WST': [0.15, 0.02, 0.05, 0.15, 0.20, 0.20, 0.05, 0.05, 0.02, 0.05, 0.05, 0.01],  # Semi-arid, sorghum/millet
        'CTR': [0.35, 0.10, 0.10, 0.08, 0.05, 0.02, 0.08, 0.08, 0.02, 0.02, 0.02, 0.08],  # Capital region
        'LKS': [0.20, 0.20, 0.15, 0.10, 0.05, 0.02, 0.08, 0.08, 0.02, 0.02, 0.02, 0.06],  # Lake fishing + agriculture
    }

    # Farm gate prices (DKW per kg)
    crop_prices = {
        'C01': 35, 'C02': 55, 'C03': 15, 'C04': 85, 'C05': 30, 'C06': 28,
        'C07': 20, 'C08': 90, 'C09': 250, 'C10': 120, 'C11': 65, 'C12': 45
    }

    records = []
    hh_id = 8000

    for i in range(n_farms):
        # New household every 1-3 plots
        if i % np.random.randint(1, 4) == 0:
            hh_id += 1

        province = np.random.choice(provinces['province_code'], p=province_weights)
        prov_districts = districts[districts['province_code'] == province]['district_name'].tolist()
        district = random.choice(prov_districts)

        # Select crop based on province
        crop_weights = province_crop_weights[province]
        crop_idx = np.random.choice(len(crops), p=crop_weights)
        crop_code, crop_name, base_yield, typical_area = crops[crop_idx]

        # Area (log-normal, smallholder dominated)
        area_hectares = round(np.random.lognormal(np.log(typical_area), 0.5), 2)
        area_hectares = max(0.1, min(area_hectares, 20))  # Cap between 0.1 and 20 ha

        # Input usage (correlated with each other and area)
        uses_fertilizer = np.random.random() < (0.25 + 0.1 * np.log1p(area_hectares))
        uses_irrigation = np.random.random() < (0.08 if province != 'WST' else 0.15)  # More in semi-arid
        uses_improved_seed = np.random.random() < (0.30 + 0.15 * uses_fertilizer)

        # Yield (affected by inputs)
        yield_multiplier = 1.0
        if uses_fertilizer:
            yield_multiplier *= 1.3
        if uses_irrigation:
            yield_multiplier *= 1.25
        if uses_improved_seed:
            yield_multiplier *= 1.15

        # Add random variation
        yield_kg_per_ha = int(base_yield * yield_multiplier * np.random.lognormal(0, 0.25))

        # Production
        production_kg = int(area_hectares * yield_kg_per_ha)

        # Season
        season = np.random.choice(['Main season', 'Second season'], p=[0.75, 0.25])

        # Sales (larger farms and cash crops sell more)
        if crop_code in ['C09', 'C10', 'C11']:  # Cash crops
            sold_pct = min(95, int(np.random.normal(75, 15)))
        else:
            sold_pct = max(0, min(90, int(np.random.normal(40, 20))))

        # Price (varies by ±20%)
        base_price = crop_prices[crop_code]
        price_per_kg = round(base_price * np.random.uniform(0.8, 1.2), 1)

        records.append({
            'farm_id': f"DAPS{year}-{i + 1:06d}",
            'hh_id': f"HH-{hh_id:06d}",
            'province': province,
            'district': district,
            'crop_code': crop_code,
            'crop_name': crop_name,
            'area_hectares': area_hectares,
            'production_kg': production_kg,
            'yield_kg_per_ha': yield_kg_per_ha,
            'season': season,
            'year': year,
            'uses_fertilizer': uses_fertilizer,
            'uses_irrigation': uses_irrigation,
            'uses_improved_seed': uses_improved_seed,
            'sold_pct': sold_pct,
            'price_per_kg': price_per_kg
        })

    return pd.DataFrame(records)


# Guard the side-effect printing at module import
if __name__ == "__main__":
    print(get_cities())
