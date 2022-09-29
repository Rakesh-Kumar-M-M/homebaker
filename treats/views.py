from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .models import Treat, Note, Coupon
from .forms import TreatForm, NoteForm, CouponForm
from .aws import upload_to_s3


def treat_list(request):
    treats = Treat.objects.all()
    return render(request, 'treats/list.html', context={'treats': treats})


def treat_detail(request, pk):
    treat = get_object_or_404(Treat, pk=pk)
    notes = treat.notes.filter(treat_id=treat.id)
    return render(request, 'treats/treat-detail.html', context={'treat': treat, 'notes': notes})


@login_required
def treat_new(request):
    if request.method == 'POST':
        form = TreatForm(data=request.POST)

        if form.is_valid():
            treat = form.save(commit=False)
            treat.user = request.user

            file = request.FILES.get("img_upload")
            if file is not None:
                cover_img_url = upload_to_s3(file)
                treat.cover_img = cover_img_url

            treat.save()
            messages.success(request, 'Added treat')
            return redirect('treats:treat_list')
    else:
        form = TreatForm()
    return render(request, 'treats/form.html', context={"form": form})


@login_required
def treat_edit(request, pk):
    treat = get_object_or_404(Treat, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TreatForm(instance=treat, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated treat')
            return redirect('treats:treat_list')
    else:
        form = TreatForm(instance=treat)

    return render(request, 'treats/form.html', context={"treat": treat,
                                                        "form": form})


@login_required
def treat_delete(request, pk):
    treat = get_object_or_404(Treat, pk=pk, user=request.user)
    if request.method == "POST":
        treat.delete()
        messages.success(request, 'Deleted treat')
        return redirect('treats:treat_list')
    return render(request, 'treats/delete.html', context={"treat": treat})


@login_required
def treat_note(request, pk):
    treat = get_object_or_404(Treat, id=pk)
    note = None
    if request.method == 'POST':
        form = NoteForm(data=request.POST)

        if form.is_valid():
            note = form.save(commit=False)
            note.treat = treat
            note.save()
            messages.success(request, 'Added note')
            return redirect('treats:treat_detail', pk=treat.id)
    else:
        form = NoteForm()
    return render(request, 'treats/note.html', context={'treat': treat, 'form': form, 'note': note})


@login_required
def treat_note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk)
    treat = note.treat
    if request.method == 'POST':
        form = NoteForm(instance=note, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated note')
            return redirect('treats:treat_detail', pk=treat.id)
    else:
        form = NoteForm(instance=note)

    return render(request, 'treats/note.html', context={"treat": treat, "note": note, "form": form})


@login_required
def treat_note_delete(request, pk):
    note = get_object_or_404(Note, id=pk)
    treat = note.treat
    if request.method == "POST":
        note.delete()
        messages.success(request, 'Deleted note')
        return redirect('treats:treat_detail', pk=treat.id)

    return render(request, 'treats/delete.html', context={"treat": treat, "note": note})


@login_required
def coupon_tracker(request):
    coupons = Coupon.objects.all()
    return render(request, 'coupons/tracker.html', context={'coupons': coupons})


@login_required
def coupon_detail(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    return render(request, 'coupons/coupon-detail.html', context={'coupon': coupon})


@login_required
def coupon_new(request):
    if request.method == 'POST':
        form = CouponForm(data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Added coupon')
            return redirect('treats:coupon_tracker')
    else:
        form = CouponForm()
    return render(request, 'coupons/coupon-detail.html', context={'form': form})


@login_required
def coupon_edit(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        form = CouponForm(data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Coupon updated')
            return redirect('treats:coupon_detail')
    else:
        form = CouponForm(instance=coupon)
    return render(request, 'coupons/coupon-detail.html', {'coupon': coupon, 'form': form})


@login_required
def coupon_delete(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        coupon.delete()
        messages.success(request, 'Coupon deleted')
        return redirect('treats:coupon_tracker')
    return render(request, 'treats/delete.html', context={'coupon': coupon})
