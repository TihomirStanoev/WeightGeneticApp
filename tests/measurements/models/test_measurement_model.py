from decimal import Decimal
from model_bakery import baker
from extrusion.models import Extrusion
from master_data.models import Profile, Reference
from measurements.models import Measurement, Batch


def test_calc_measured_gpm_valid_length():
    length_mm = Decimal('500.00')
    workpiece_weight_gr = Decimal('2000.00')
    expected_measured_gpm = Decimal('4000.00')

    measure = Measurement(
        length_mm=length_mm,
        workpiece_weight_gr=workpiece_weight_gr,
    )

    assert measure._calc_measured_gpm() == expected_measured_gpm


def test_calc_measured_gpm_zero_length():
    length_mm = Decimal('0.00')
    workpiece_weight_gr = Decimal('2000.00')

    measure = Measurement(
        length_mm=length_mm,
        workpiece_weight_gr=workpiece_weight_gr,
    )

    assert measure._calc_measured_gpm() is None




def test_calc_measured_gpm_none_length():
    length_mm = None
    workpiece_weight_gr = Decimal('2000.00')

    measure = Measurement(
        length_mm=length_mm,
        workpiece_weight_gr=workpiece_weight_gr,
        machined_weight_gr=Decimal('1000.00'),
    )

    assert measure._calc_measured_gpm() is None



def test_calc_k_vs_basket_valid_result():
    measured_gpm = Decimal('950.00')
    card_grm = Decimal('1000.00')
    expected_result = Decimal('0.95000')

    card = baker.prepare(
        Extrusion,
        card_grm=card_grm
    )
    measure = Measurement(
        card=card
    )

    assert measure._calc_k_vs_basket(measured_gpm) == expected_result


def test_calc_k_vs_basket_none_measured_gpm():
    measured_gpm = None

    measure = Measurement()

    assert measure._calc_k_vs_basket(measured_gpm) is None



def test_calc_k_vs_theoretical_valid_result():
    measured_gpm = Decimal('950.00')
    theoretical_gpm = Decimal('1000.00')
    expected_result = Decimal('0.95000')

    profile = baker.prepare(
        Profile,
        theoretical_gpm=theoretical_gpm
    )

    card = baker.prepare(
        Extrusion,
        profile=profile
    )

    measure = Measurement(
        card=card
    )

    assert measure._calc_k_vs_theoretical(measured_gpm) == expected_result



def test_calc_k_vs_theoretical_none_measured_gpm():
    measured_gpm = None

    measure = Measurement()

    assert measure._calc_k_vs_theoretical(measured_gpm) is None



def test_calc_workpiece_delta_pct_valid_blank_theoretical():
    workpiece_weight_gr = Decimal('525')
    blank_theoretical = Decimal('500')
    expected_result = Decimal('5')

    measure = Measurement(
        workpiece_weight_gr = workpiece_weight_gr
    )

    assert measure._calc_workpiece_delta_pct(blank_theoretical) == expected_result



def test_calc_workpiece_delta_pct_none_blank_theoretical():
    blank_theoretical = None

    measure = Measurement()

    assert measure._calc_workpiece_delta_pct(blank_theoretical) is None



def test_calc_reference_delta_pct_valid_result():
    k_vs_theoretical = Decimal('1.10')
    machined_weight_gr = Decimal('121')
    theoretical_weight = Decimal('100')
    expected_result = Decimal('10')

    reference = baker.prepare(
        Reference,
        theoretical_weight=theoretical_weight,
    )
    batch = baker.prepare(
        Batch,
        reference=reference,
    )
    measure = Measurement(
        machined_weight_gr=machined_weight_gr,
        batch=batch,
    )

    assert measure._calc_reference_delta_pct(k_vs_theoretical) == expected_result


def test_calc_reference_delta_pct_none_machined_weight():
    measure = Measurement(machined_weight_gr=None)

    assert measure._calc_reference_delta_pct(Decimal('1.10')) is None


def test_calc_reference_delta_pct_none_k_vs_theoretical():
    measure = Measurement(machined_weight_gr=Decimal('121'))

    assert measure._calc_reference_delta_pct(None) is None


def test_calc_reference_delta_pct_zero_k_vs_theoretical():
    measure = Measurement(machined_weight_gr=Decimal('121'))

    assert measure._calc_reference_delta_pct(Decimal('0')) is None


def test_calc_reference_delta_pct_zero_theoretical_weight():
    reference = baker.prepare(
        Reference,
        theoretical_weight=Decimal('0'),
    )
    batch = baker.prepare(
        Batch,
        reference=reference,
    )
    measure = Measurement(
        machined_weight_gr=Decimal('121'),
        batch=batch,
    )

    assert measure._calc_reference_delta_pct(Decimal('1.10')) is None
