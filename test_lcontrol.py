import hb_menu
import hb_encoder

debug_argument = 1
rotate = 0

def l_control_newtype(light):
    #This is the prototype for how I want t pote3ntially do this in the future
    result = 0
    #menu_layout = ("Light: "+str(light), "Bri: ",
    #                calc_func = bri_calc, c_param = "encoder_pos",
    #                action_func = hue_lights, a_param = "bri",
    #                min_val = 0, max_val = 10, #or maybe use range(0,100)? this is the encoder value btw, not screen value
    #                timeout = 100, timeout_func = timedout)
    menu = hb_menu.Menu_Creator(debug = debug_argument, menu_layout = None, rotate = rotate)
    result = menu.single_value_menu("Light: "+str(light), "Bri: ",
                                    calc_func = bri_calc, rev_calc = rev_bri_calc,
                                    action_func = hue_lights,
                                    start_pos = get_start_pos(), a_param = "bri",
                                    min_val = 0, max_val = 10, #or maybe use range(0,100)? this is the encoder value btw, not screen value
                                    timeout = 5000, timeout_func = timedout)
    encoder.wait_for_button_release()
    return

def get_start_pos():
    #do something and math to get start position
    start_pos = rev_bri_calc(0)
    return int(start_pos)

def bri_calc(encoder_pos):
    brightness = encoder_pos * 10.16
    return int(brightness)

def rev_bri_calc(brightness):
    encoder_pos = brightness / 10.16
    return int(encoder_pos)

def hue_lights(bri):
    print ("in hue lights: something hue lights: "+str(bri))
    return

def timedout(encoder_pos):
    print("in timed out: timed out on " + str(encoder_pos))
    return


if __name__ == '__main__':
    encoder = hb_encoder.RotaryClass(debug = debug_argument)
    l_control_newtype(1)
    print("lol finished")
