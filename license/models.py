from django.db import models

# Create your models here.


class License(models.Model):
    name = models.CharField(max_length=300)
    subtitle = models.CharField(max_length=500)
    description = models.TextField()
    


class TrackOwnerLicense(models.Model):
    
    GENDER_CHOICE = [
        ("Male","Male"),
        ("Female","Female"),
    ]

    surname = models.CharField(max_length=500)
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    address = models.TextField()
    postal_code = models.CharField(max_length=500)
    dob = models.DateField()
    phone_number = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    nationality = models.CharField(max_length=500)
    gender = models.CharField(choices= GENDER_CHOICE, max_length=500)
    
    track_location = models.CharField(max_length=500)
    track_name = models.CharField(max_length=500)
    surface_type = models.CharField(max_length=500)
    length_of_track_km = models.DecimalField(max_digits=8, decimal_places=2)
    number_of_lanes = models.IntegerField()
    last_inspection_date = models.DateField()
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    
    is_insurred = models.CharField(max_length=5)
    issurance_provider = models.CharField(max_length=200)
    policy_number = models.CharField(max_length=200)
    expiring_date = models.DateField()
    insurance_cerificate = models.FileField()

    frequecy_of_maintenance = models.CharField(max_length=300),
    safely_protocols = models.TextField()
    maintenance_logs_file = models.FileField()
    
    
    signature = models.FileField()
    date = models.DateField( auto_now=False, auto_now_add=False)
    
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_by = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)
    is_approved = models.BooleanField(default=False)

class EventPromoterLicense(models.Model):
    
    GENDER_CHOICE = [
        ("Male","Male"),
        ("Female","Female"),
    ]

    surname = models.CharField(max_length=500)
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    company_name = models.CharField(max_length=500)
    position = models.DateField()
    phone_number = models.CharField(max_length=500)
    address = models.TextField()
    email = models.CharField(max_length=500)

    
    event_location = models.CharField(max_length=500)
    event_name = models.CharField(max_length=500)
    dates_of_events = models.TextField()
    estimate_participants = models.IntegerField()
    estimate_spectators = models.IntegerField()
    event_type = models.CharField(max_length=500)
    track_license_number = models.CharField(max_length=500)
    
    conducted_risk_assessment = models.CharField(max_length=50)
    emergency_contacts = models.CharField(max_length=200)
    safety_measure_description = models.TextField()
    medical_support_arrangement = models.TextField()

    
    insurance_coverage = models.CharField(max_length=50)
    insurance_provider = models.CharField(max_length=200)
    policy_number = models.TextField()
    expiering_date = models.DateField()
    insurance_certificate_image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    
    signature = models.FileField()
    date = models.DateField( auto_now=False, auto_now_add=False)
    
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_by = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)
    is_approved = models.BooleanField(default=False)
    

class RacingLicense(models.Model):
    
    GENDER_CHOICE = [
        ("Male","Male"),
        ("Female","Female"),
    ]

    surname = models.CharField(max_length=500)
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    address = models.TextField()
    postal_code = models.CharField(max_length=500)
    dob = models.DateField()
    phone_number = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    nationality = models.CharField(max_length=500)
    gender = models.CharField(choices= GENDER_CHOICE, max_length=500)
    disability = models.CharField(max_length=500)
    licenses = models.ManyToManyField(License)
    
    vision_test = models.ImageField(null=True, blank=True)
    

class EmergencyContact(models.Model):
    application = models.ForeignKey(RacingLicense, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    address = models.TextField()
    

class Children(models.Model):
    full_name = models.CharField(max_length=500)
    dob = models.DateField(auto_now=False, auto_now_add=False)


class Guardian(models.Model):
    application = models.ForeignKey(RacingLicense, on_delete=models.CASCADE)
    surname = models.CharField(max_length=500)
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    address = models.TextField()
    postal_code = models.CharField(max_length=500)
    dob = models.DateField()
    phone_number = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    
    children = models.ManyToManyField(Children)
    
    

class MedicalDeclaration(models.Model):
    
    YES_NO = [
        ("YES", "YES"),
        ("NO", "NO"),
    ]
    
    application = models.ForeignKey(RacingLicense, on_delete=models.CASCADE)
    any_restrictions_imposed_on_life_assurance = models.CharField(max_length=5, choices=YES_NO)
    taken_any_substances_listed_on_WADA_problist = models.CharField(max_length=5, choices=YES_NO)
    history_of_drug_or_alcohol_abuse = models.CharField(max_length=5, choices=YES_NO)
    severe_allergic_reaction_requiring_hospital_treatment = models.CharField(max_length=5, choices=YES_NO)
    diabetes_or_received_treatment_with_insulin = models.CharField(max_length=5, choices=YES_NO)
    neurological_disorder_including_epilepsy_and_or_others = models.CharField(max_length=5, choices=YES_NO)
    obstructive_sleep_apnea_or_narcolepsy = models.CharField(max_length=5, choices=YES_NO)
    serious_head_injury_or_concussion = models.CharField(max_length=5, choices=YES_NO)
    had_a_stroke_or_CVA_or_TIA = models.CharField(max_length=5, choices=YES_NO)
    heart_disease_or_any_heart_disorder = models.CharField(max_length=5, choices=YES_NO)
    heart_attack_myocardial_infarction_or_undergone_cardiac_surgery = models.CharField(max_length=5, choices=YES_NO)
    anticoagulant_drugs_excluding_aspirin = models.CharField(max_length=5, choices=YES_NO)
    implanted_medical_devices = models.CharField(max_length=5, choices=YES_NO)
    psychiatric_illness_mental_health_condition_or_depression = models.CharField(max_length=5, choices=YES_NO)
    neurodevelopmental_condition_ADHD_or_ASD = models.CharField(max_length=5, choices=YES_NO)
    limb_congenital_abnormality_permanent_difficulty_using_your_arms_legs = models.CharField(max_length=5, choices=YES_NO)
    corrective_lense_during_driving = models.CharField(max_length=5, choices=YES_NO)
    deaf_unable_to_hear = models.CharField(max_length=5, choices=YES_NO)
    surgical_procedure_in_last_two_years = models.CharField(max_length=5, choices=YES_NO)
    diagnosed_with_condition_affecting_vehicle_control = models.CharField(max_length=5, choices=YES_NO)
    
    height_in_cm = models.DecimalField(decimal_places=2, max_digits=5)
    weight_in_kg = models.DecimalField(decimal_places=2, max_digits=5)
    details = models.TextField(null=True, blank=True)
    
    
class LicenseApplicationSignature(models.Model):
    application = models.ForeignKey(RacingLicense, on_delete=models.CASCADE)
    child = models.ForeignKey(Children, on_delete=models.CASCADE, null=True, blank=True)
    
    applicant_signature = models.ImageField()
    parent_signature_under18 = models.ImageField(null=True, blank=True)
    parent_signature_entrantPF = models.ImageField(null=True, blank=True)
    
    date = models.DateField()