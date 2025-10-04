from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket, Comment
from .forms import TicketForm, CommentForm
from datetime import date
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

@login_required
def ticket_list(request):
   
   if request.user.is_staff:
        tickets = Ticket.objects.all()
   else:
        tickets = Ticket.objects.filter(
            models.Q(user=request.user) |
            models.Q(user__is_staff=True)
        )
   return render(request, 'tickets/ticket_list.html', {'tickets': tickets, 'today': date.today()})
@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if not (ticket.user == request.user or request.user.is_staff):
        return render(request, 'tickets/ticket_detail.html', {'ticket': ticket, 'can_edit': False})


    comments = ticket.comments.all().order_by('created_at')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.user = request.user
            comment.save()
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = CommentForm()
    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'comments': comments,
        'form': form,
        'today': date.today()
    })

    ticket = get_object_or_404(Ticket, pk=pk)
    comments = ticket.comments.all().order_by('created_at')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.user = request.user
            comment.save()
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = CommentForm()
    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'comments': comments,
        'form': form
    })

@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('ticket_list')
    else:
        form = TicketForm()
    return render(request, 'tickets/ticket_form.html', {'form': form})
@login_required
def ticket_edit(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if not (ticket.user == request.user or request.user.is_staff):
        raise PermissionDenied("You do not have permission to edit this ticket.")

    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'tickets/ticket_form.html', {'form': form, 'edit_mode': True})