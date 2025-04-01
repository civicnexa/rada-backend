from rest_framework import serializers

from license.models import EventPromoterLicense, TrackOwnerLicense


class TrackOwnerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackOwnerLicense
        exclude = ["is_approved", "updated_by"]
        # fields =


class TrackOwnerRegistrationSerializerOut(serializers.ModelSerializer):
    class Meta:
        model = TrackOwnerLicense
        exclude = ["updated_by"]
        # fields =


class ListTrackOwnerSerializerOut(serializers.ModelSerializer):
    class Meta:
        model = TrackOwnerLicense
        # exclude = ["updated_by"]
        fields = ["track_location", "track_name", "surface_type", "length_of_track_km",]


class TrackOwnerDetailSerializerOut(serializers.ModelSerializer):
    class Meta:
        model = TrackOwnerLicense
        fields = ["track_location", "track_name", "surface_type", "length_of_track_km",
                    "number_of_lanes", "last_inspection_date", "image", "is_insurred",
                    "insurance_cerificate", "policy_number", "safely_protocols", ]


class EventPromoterRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPromoterLicense
        exclude = ["is_approved", "updated_by"]
        # fields =

    def create(self, validated_data):
        return super().create(validated_data)
    
    
class EventPromoterRegistrationSerializerOut(serializers.ModelSerializer):
    class Meta:
        model = EventPromoterLicense
        exclude = ["updated_by"]
        # fields =


class ListEventPromoterSerializerOut(serializers.ModelSerializer):
    class Meta:
        model = EventPromoterLicense
        exclude = ["updated_by"]
        fields = ["event_location", "event_name", "dates_of_events", "estimate_participants", "event_type"]


class EventPromoterDetailSerializerOut(serializers.ModelSerializer):
    class Meta:
        model = EventPromoterLicense
        exclude = ["updated_by"]
        fields = ["event_location", "event_name", "dates_of_events", "estimate_participants", 
            "estimate_spectators", "event_type", "track_license_number", "conducted_risk_assessment",
            "emergency_contacts", "safety_measure_description", "medical_support_arrangement", "insurance_coverage",
            "insurance_provider", "policy_number", "expiering_date", "insurance_certificate_image",]