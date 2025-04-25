from math import pi, sin, cos
from pyglet.math import Mat4, Vec3


def sinwaveSnake(current_t, phase, height, width, frequency):
    a = []
    for i in range(8):
        a.append( (3+i*i/3)/6 * height * sin(current_t/width + phase + i*frequency))
    
    wave_angles = { # format:[bend, tilt]
        "wb1" : Mat4(),
        "b1n1" : [0.02*pi, 0], # body1 > neck1  
        "n1n2" : [0.02*pi, 0], # neck1 > neck2
        "n2n3" : [-0.05*pi, 0], # neck2 > neck3
        "n3h" : [0, 0], # neck3 > head
        "hj" : [0, 0], # neck3 > jaw
        "b1b2" : [0, a[3]], # body1 > body2
        "b2b3" : [0, a[4]], # body2 > body3
        "b3b4" : [0, a[5]], # body3 > body4
        "b4b5" : [0, a[6]], # body4 > body5
        "b5t" : [0, a[7]],  # body5 > tail   \
        "n1wL" : 0, # neck1 > wingL
        "n1wR" : 0, # neck1 > wingR
        "n2wL" : 0, # neck2 > wingL
        "n2wR" : 0, # neck2 > wingR
        "n3wL" : 0, # neck3 > wingL
        "n3wR" : 0 # neck3 > wingR
    }

    angles = wave_angles

    return angles

def raisehead(start_angles, current_t, start_t, end_t):
    end_angles = raisehead_angles
    intermidiate_angles = interpolation(start_angles, end_angles, (current_t-start_t)/(end_t-start_t))

    return intermidiate_angles    

def lowerhead(start_angles, current_t, start_t, end_t):
    end_angles = rest_angles
    intermidiate_angles = interpolation(start_angles, end_angles, (current_t-start_t)/(end_t-start_t))

    return intermidiate_angles  

def attack(start_angles, current_t, start_t, end_t):
    end_angles = attack_angles
    if (current_t-start_t)/(end_t-start_t) <= 0.5:
        intermidiate_angles = interpolation(start_angles, end_angles, 2*(current_t-start_t)/(end_t-start_t))
    else:
        intermidiate_angles = interpolation(end_angles, start_angles,  2*(current_t-(start_t+end_t)/2)/(end_t-start_t))

    return intermidiate_angles 

def superposition(angles1, angles2):
    "define non-commutative superposition between 2 control inputs."
    summed_angles = {}
    for key in angles1.keys() | angles2.keys():  # Union of keys
        val1 = angles1.get(key, [0, 0] if isinstance(angles1.get(key), list) else 0)
        val2 = angles2.get(key, [0, 0] if isinstance(angles2.get(key), list) else 0)
        
        if isinstance(val1, list) and isinstance(val2, list):
            summed_angles[key] = [val1[0] + val2[0], val1[1] + val2[1]]
        elif isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
            summed_angles[key] = val1 + val2
        else:
            summed_angles[key] = val2 @ val1
    
    return summed_angles

def interpolation(angles1, angles2, p):
    "define interpolation between 1 angle to another. extrapolation is not supported"
    inter_angles = {}
    for key in angles1.keys() | angles2.keys():  # Union of keys
        val1 = angles1.get(key, [0, 0] if isinstance(angles1.get(key), list) else 0)
        val2 = angles2.get(key, [0, 0] if isinstance(angles2.get(key), list) else 0)

        if p < 0:
            return angles1
        elif p > 1:
            return angles2
        else:
            if isinstance(val1, list) and isinstance(val2, list):
                inter_angles[key] = [(1-p)*val1[0] + p*val2[0], (1-p)*val1[1] + p*val2[1]]
            elif isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                inter_angles[key] = (1-p)*val1 + p*val2
            else:
                inter_angles[key] = val2 @ val1
    
    return inter_angles

attack_angles = { # format:[bend, tilt]
    "wb1" : Mat4(),
    "b1n1" : [0.2*pi, 0], # body1 > neck1  
    "n1n2" : [-0.2*pi, 0], # neck1 > neck2
    "n2n3" : [-0.2*pi, 0], # neck2 > neck3
    "n3h" : [-0.1*pi, 0], # neck3 > head
    "hj" : [0.1*pi, 0], # neck3 > jaw
    "b1b2" : [0, 0], # body1 > body2
    "b2b3" : [0, 0], # body2 > body3
    "b3b4" : [0, 0], # body3 > body4
    "b4b5" : [0, 0], # body4 > body5
    "b5t" : [0, 0],  # body5 > tail   \
    "n1wL" : 0.1*pi, # neck1 > wingL
    "n1wR" : 0.1*pi, # neck1 > wingR
    "n2wL" : 0.1*pi, # neck2 > wingL
    "n2wR" : 0.1*pi, # neck2 > wingR
    "n3wL" : 0.1*pi, # neck3 > wingL
    "n3wR" : 0.1*pi # neck3 > wingR
}

raisehead_angles = { # format:[bend, tilt]
    "wb1" : Mat4(),
    "b1n1" : [0.2*pi, 0], # body1 > neck1  
    "n1n2" : [0.2*pi, 0], # neck1 > neck2
    "n2n3" : [-0.4*pi, 0], # neck2 > neck3
    "n3h" : [-0.2*pi, 0], # neck3 > head
    "hj" : [-0.3*pi, 0], # neck3 > jaw
    "b1b2" : [0, 0], # body1 > body2
    "b2b3" : [0, 0], # body2 > body3
    "b3b4" : [0, 0], # body3 > body4
    "b4b5" : [0, 0], # body4 > body5
    "b5t" : [0, 0],  # body5 > tail   \
    "n1wL" : -0.05*pi, # neck1 > wingL 
    "n1wR" : -0.05*pi, # neck1 > wingR
    "n2wL" : -0.05*pi, # neck2 > wingL
    "n2wR" : -0.05*pi, # neck2 > wingR
    "n3wL" : -0.05*pi, # neck3 > wingL
    "n3wR" : -0.05*pi # neck3 > wingR
}

rest_angles = { # format:[bend, tilt]
    "wb1" : Mat4(),
    "b1n1" : [0.05*pi, 0], # body1 > neck1  
    "n1n2" : [0.05*pi, 0], # neck1 > neck2
    "n2n3" : [-0.1*pi, 0], # neck2 > neck3
    "n3h" : [0, 0], # neck3 > head
    "hj" : [-0.1*pi, 0], # neck3 > jaw
    "b1b2" : [0, 0], # body1 > body2
    "b2b3" : [0, 0], # body2 > body3
    "b3b4" : [0, 0], # body3 > body4
    "b4b5" : [0, 0], # body4 > body5
    "b5t" : [0, 0],  # body5 > tail   \
    "n1wL" : 0, # neck1 > wingL
    "n1wR" : 0, # neck1 > wingR
    "n2wL" : 0, # neck2 > wingL
    "n2wR" : 0, # neck2 > wingR
    "n3wL" : 0, # neck3 > wingL
    "n3wR" : 0 # neck3 > wingR
}

null_angles = { # format:[bend, tilt]
    "wb1" : Mat4(), 
    "b1n1" : [0, 0], # body1 > neck1  
    "n1n2" : [0, 0], # neck1 > neck2
    "n2n3" : [0, 0], # neck2 > neck3
    "n3h" : [0, 0], # neck3 > head
    "hj" : [0, 0], # neck3 > jaw
    "b1b2" : [0, 0], # body1 > body2
    "b2b3" : [0, 0], # body2 > body3
    "b3b4" : [0, 0], # body3 > body4
    "b4b5" : [0, 0], # body4 > body5
    "b5t" : [0, 0],  # body5 > tail   \
    "n1wL" : 0, # neck1 > wingL
    "n1wR" : 0, # neck1 > wingR
    "n2wL" : 0, # neck2 > wingL
    "n2wR" : 0, # neck2 > wingR
    "n3wL" : 0, # neck3 > wingL
    "n3wR" : 0 # neck3 > wingR
}