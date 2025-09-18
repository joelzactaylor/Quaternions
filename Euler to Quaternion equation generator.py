import sympy as sp


A1, A2, A3, B1, B2, B3 = sp.symbols('A1 A2 A3 B1 B2 B3')


def euler_to_quaternion(order):
    return [
            [
                [[B1, B2, B3][axis], [A1, A2, A3][axis], 0, 0],
                [[B1, B2, B3][axis], 0, [A1, A2, A3][axis], 0],
                [[B1, B2, B3][axis], 0, 0, [A1, A2, A3][axis]],
                ][['X', 'Y', 'Z'].index(order[axis])]
            for axis in range(3)
        ]

    
    
# For quaternion multiplication
def quaternion_multiply(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return [
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2
    ]

# Now compute the quaternion for each of the 12 orders
orders = [
    'XYZ', 'ZYX', 'YZX', 'XZY', 'YXZ', 'ZXY', 
    'ZYZ', 'XYX', 'YXY', 'XZX', 'ZXZ', 'YZY'
]


quaternions = {}


for order in orders:
    q1, q2, q3 = euler_to_quaternion(order)
    quaternions[order] = quaternion_multiply(quaternion_multiply(q3, q2), q1)
    
    

# Display the results in terms of the symbolic formulas
for order, quaternion in quaternions.items():
    print(f"Quaternion for Euler order {order}:")
    for i, component in enumerate(quaternion):
        print(f"Q{['w', 'x', 'y', 'z'][i]}: {component}")
    print()



