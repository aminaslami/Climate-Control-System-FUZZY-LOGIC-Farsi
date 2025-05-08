# بار گیری کتابخانه های ضروری
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import networkx as nx

# خطای دمایی (مطلوب - فعلی) جهان و توابع عضویت را تعریف کنید
temperature_error = ctrl.Antecedent(np.arange(-10, 10.1, 0.1), 'temperature_error')
control_signal = ctrl.Consequent(np.arange(-1, 1.1, 0.1), 'control_signal')

# temperature_error توابع عضویت برای
temperature_error['nb'] = fuzz.trimf(temperature_error.universe, [-10, -10, -5])  # منفی بزرگ
temperature_error['ns'] = fuzz.trimf(temperature_error.universe, [-10, -5, 0])    # منفی کوچک
temperature_error['ze'] = fuzz.trimf(temperature_error.universe, [-5, 0, 5])      # صفر
temperature_error['ps'] = fuzz.trimf(temperature_error.universe, [0, 5, 10])      # مثبت کوچک
temperature_error['pb'] = fuzz.trimf(temperature_error.universe, [5, 10, 10])     # مثبت بزرگ

# control_signal توابع عضویت برای
control_signal['cool_high'] = fuzz.trimf(control_signal.universe, [-1, -1, -0.5]) # خنک زیاد
control_signal['cool_low'] = fuzz.trimf(control_signal.universe, [-1, -0.5, 0])   # خنک کم
control_signal['no_action'] = fuzz.trimf(control_signal.universe, [-0.5, 0, 0.5]) # بدون فعالیت
control_signal['heat_low'] = fuzz.trimf(control_signal.universe, [0, 0.5, 1])     # گرم کردن کم
control_signal['heat_high'] = fuzz.trimf(control_signal.universe, [0.5, 1, 1])    # گرم کردن زیاد

# قوانین فازی
rule1 = ctrl.Rule(temperature_error['nb'], control_signal['cool_high'])  # اگر خطا[ان-بی] است، محکم خنک کنید 
rule2 = ctrl.Rule(temperature_error['ns'], control_signal['cool_low'])   # اگر خطا [ان-سی] است، نرم خنک کنید
rule3 = ctrl.Rule(temperature_error['ze'], control_signal['no_action'])  # اگر خطا [ان-ای] است، هیچ اقدامی انجام ندهید
rule4 = ctrl.Rule(temperature_error['ps'], control_signal['heat_low'])   # اگر خطا [پی-اس] است، نرم گرم کنید
rule5 = ctrl.Rule(temperature_error['pb'], control_signal['heat_high'])  # اگر خطا [پی-بی] است، محکم گرم کنید

# ایجاد سیستم کنترل
climate_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
climate_sim = ctrl.ControlSystemSimulation(climate_ctrl)

def main():
    print("سیستم کنترل آب و هوا با منطق فازی")
    print("برای محاسبه سیگنال کنترل، دمای فعلی و دمای مورد نظر را وارد کنید.")
    
    while True:
        try:
            current_temp = float(input("\nدمای فعلی را وارد کنید (°C): "))
            desired_temp = float(input("دمای مورد نظر را وارد کنید (°C): "))
        except ValueError:
            print("ورودی نامعتبر است. لطفا اعداد را وارد کنید.")
            continue
        
        error = desired_temp - current_temp
        climate_sim.input['temperature_error'] = error
        
        try:
            climate_sim.compute()
        except Exception as e:
            print(f"خطا در محاسبه: {e}. لطفا ورودی‌ها را بررسی کنید.")
            continue
        
        output = climate_sim.output['control_signal']
        
        # اقدام را تعیین کنید
        if output > 0:
            action = f"گرمایش در {output * 100:.1f}%"
        elif output < 0:
            action = f"خنک سازی در {-output * 100:.1f}%"
        else:
            action = "نیازی به اقدام نیست."
        
        print(f"خطای دما: {error:.1f}°C")
        print(f"سیگنال کنترل: {output:.2f}")
        print(f"اکشن (عکس العمل): {action}")

if __name__ == "__main__":
    main()