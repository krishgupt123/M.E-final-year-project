from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, Patient_info_Form, UpdateUserForm, UpdateProfileForm,UserPredictForm
from .models import UserPredictModel, Patient_info, Profile

from PIL import Image, ImageOps
import numpy as np
import joblib
from tensorflow import keras


# ---------------------- Static Pages ----------------------

def Landing_1(request):
    return render(request, '1_Landing.html')

def Home_4(request):
    return render(request, '4_Home.html')

def Teamates_5(request):
    return render(request, '5_Teamates.html')

def report(request):
    return render(request, 'report.html')


# ---------------------- User Registration ----------------------

def Register_2(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for {user}')
            return redirect('Login_3')

    return render(request, '2_Register.html', {'form': form})


# ---------------------- User Login ----------------------

def Login_3(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('Home_4')
        else:
            messages.error(request, 'Username or Password is incorrect')

    return render(request, '3_Login.html')


# ---------------------- Profile View & Edit ----------------------

@login_required(login_url='Login_3')
def profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')

    else:
        user_form = UpdateUserForm(instance=user)
        profile_form = UpdateProfileForm(instance=profile)

    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import numpy as np
from tensorflow import keras
from PIL import Image, ImageOps
import pyttsx3

from .models import UserPredictModel
from .forms import UserPredictForm

def Deploy_10(request):
    print("HI")
    
    if request.method == "POST":
        form = UserPredictForm(request.POST, request.FILES)
        if form.is_valid():
            print('HIFORM')
            form.save()
            obj = form.instance

            # Load the latest saved image for prediction
            latest_prediction = UserPredictModel.objects.latest('id')
            model = keras.models.load_model('APP/keras_model.h5')

            # Prepare the image
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            image = Image.open("media/" + str(latest_prediction.image)).convert("RGB")
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)  # updated for Pillow 10+
            image_array = np.asarray(image)
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
            data[0] = normalized_image_array

            # Make prediction
            classes = ['Cyst', 'Normal', 'Stone', 'Tumor']
            prediction = model.predict(data)
            prediction_index = np.argmax(prediction)
            result_label = classes[prediction_index]

            # Add voice message using pyttsx3
            if result_label == 'Cyst':
                message = 'THE KIDNEY CANCER TYPE OF CYST AFFECTED'
            elif result_label == 'Normal':
                message = 'NORMAL'
            elif result_label == 'Stone':
                message = 'THE KIDNEY CANCER TYPE OF A STONE AFFECTED'
            elif result_label == 'Tumor':
                message = 'THE KIDNEY CANCER TYPE OF A TUMOR AFFECTED'
            else:
                message = 'WRONG INPUT'

            # Speak the result
            engine = pyttsx3.init()
            engine.say(message)
            engine.runAndWait()

            # Save result to model
            latest_prediction.label = message
            latest_prediction.save()

            return render(request, 'result.html', {
                'form': form,
                'obj': obj,
                'predict': message
            })
    else:
        form = UserPredictForm()
        
    return render(request, '10_Deploy.html', {'form': form})

import numpy as np
import joblib
from django.shortcuts import render
from django.utils import timezone
from .models import PatientRecord

Model = joblib.load('APP/model.pkl')

def Deploy_9(request):
    if request.method == "POST":
        # Extract all values except csrf_token
        int_features = [x for x in request.POST.values()]
        int_features = int_features[1:]  # remove csrf_token
        print("Form values:", int_features)

        # Convert to numpy array
        final_features = [np.array(int_features, dtype=float)]
        prediction = Model.predict(final_features)
        output = prediction[0]
        print(f'Model Output: {output}')

        # Determine prediction text
        if output == 0.0:
            prediction_text = "THE PATIENT MIGHT NOT GO IN THE STATE OF DANGEROUS ZONE. THIS IS COMPLETELY SAFE ZONE."
        elif output == 1:
            prediction_text = "THE PATIENT MIGHT GO IN THE STATE OF MEDIUM LEVEL ZONE."
        elif output == 2:
            prediction_text = "THE PATIENT MIGHT GO IN THE STATE OF DANGEROUS ZONE. WE SHOULD TAKE TREATMENTS TO THIS PATIENT IMMEDIATELY"
        else:
            prediction_text = "Prediction could not be determined."

        # Save record to database
        try:
            PatientRecord.objects.create(
                age=float(int_features[0]),
                gender=float(int_features[1]),
                BMI=float(int_features[2]),
                hypertensive=float(int_features[3]),
                diabetes=float(int_features[4]),
                depression=float(int_features[5]),
                heart_rate=float(int_features[6]),
                systolic_bp=float(int_features[7]),
                diastolic_bp=float(int_features[8]),
                respiratory_rate=float(int_features[9]),
                temperature=float(int_features[10]),
                sp_o2=float(int_features[11]),
                urine_output=float(int_features[12]),
                rbc=float(int_features[13]),
                mch=float(int_features[14]),
                mchc=float(int_features[15]),
                mcv=float(int_features[16]),
                rdw=float(int_features[17]),
                creatinine=float(int_features[18]),
                urea_nitrogen=float(int_features[19]),
                glucose=float(int_features[20]),
                blood_potassium=float(int_features[21]),
                blood_sodium=float(int_features[22]),
                blood_calcium=float(int_features[23]),
                chloride=float(int_features[24]),
                magnesium_ion=float(int_features[25]),
                PH=float(int_features[26]),
                lactic_acid=float(int_features[27]),
                PCO2=float(int_features[28]),
                prediction_text=prediction_text,
                created_at=timezone.now()
            )
        except Exception as e:
            print("Error saving record:", e)

        return render(request, '8_Per_Info.html', {"prediction_text": prediction_text})

    return render(request, '9_Deploy.html')


def res(request):
    
    return render(request,'result.html')








def Logout(request):
    logout(request)
    return redirect('/')






from .models import Patient_info

def patient_list(request):
    patients = Patient_info.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})

def database(request):
    models = UserPredictModel.objects.all()
    return render(request, 'img_database.html', {'models':models})

def matrix(request):
    return render(request,'matrix.html')