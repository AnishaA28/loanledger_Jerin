from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Loan, Repayment
from .serializers import (
    AddRepaymentSerializer,
    CreateLoanSerializer,
    LoanSerializer,
    RepaymentSerializer,
)


@api_view(['GET', 'POST'])
def loans_list(request):
    """GET all loans (newest first) | POST create a loan."""
    if request.method == 'GET':
        loans = Loan.objects.all()
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)

    serializer = CreateLoanSerializer(data=request.data)
    if serializer.is_valid():
        loan = serializer.save()
        return Response(LoanSerializer(loan).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def loan_detail(request, pk):
    """GET a single loan | DELETE it."""
    loan = get_object_or_404(Loan, pk=pk)

    if request.method == 'GET':
        return Response(LoanSerializer(loan).data)

    loan.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def repayments(request, pk):
    """GET repayments for a loan | POST add a repayment."""
    loan = get_object_or_404(Loan, pk=pk)

    if request.method == 'GET':
        reps = loan.repayments.all()
        return Response(RepaymentSerializer(reps, many=True).data)

    serializer = AddRepaymentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    amount = serializer.validated_data['amount_returned']
    if amount > loan.pending_amount:
        return Response(
            {'error': f'Repayment amount exceeds pending ₹{loan.pending_amount}'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Create repayment record
    repayment = Repayment.objects.create(
        loan=loan,
        amount_returned=amount,
        return_date=serializer.validated_data['return_date'],
        notes=serializer.validated_data.get('notes', ''),
    )

    # Update loan totals
    loan.total_returned += amount
    loan.save()  # save() recomputes pending_amount and status

    return Response(RepaymentSerializer(repayment).data, status=status.HTTP_201_CREATED)
