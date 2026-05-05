from rest_framework import serializers
from .models import Loan, Repayment


class RepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repayment
        fields = ['id', 'loan_id', 'amount_returned', 'return_date', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            'id', 'given_to', 'amount_given', 'given_date',
            'total_returned', 'pending_amount', 'status', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'total_returned', 'pending_amount', 'status', 'created_at']


class CreateLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['given_to', 'amount_given', 'given_date', 'notes']

    def create(self, validated_data):
        validated_data['total_returned'] = 0
        validated_data['pending_amount'] = validated_data['amount_given']
        return super().create(validated_data)


class AddRepaymentSerializer(serializers.Serializer):
    amount_returned = serializers.IntegerField(min_value=1)
    return_date = serializers.DateField()
    notes = serializers.CharField(allow_blank=True, default='')
