from manim import *
from math import atan, sin, cos, sqrt
import numpy as np

my_tex_template = TexTemplate()
my_tex_template.add_to_preamble(r"\usepackage{xcolor}")
my_tex_template.add_to_preamble(r"\usepackage[usenames,dvipsnames]{xcolor}")
my_tex_template.add_to_preamble(r"\usepackage[HTML]{xcolor}")
my_tex_template.add_to_preamble(r"\definecolor{vibrantpurple}{HTML}{9B30FF}")
my_tex_template.add_to_preamble(r"\definecolor{brightblue}{HTML}{1E90FF}")


class EulerOrderExample(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()

        x_label = axes.get_x_axis_label(Tex("x"))
        y_label = axes.get_y_axis_label(Tex("y")).shift(UP * 1.8)


        # zoom out so we see the axes
        self.set_camera_orientation(zoom=0.5)

        self.play(FadeIn(axes), FadeIn(x_label), FadeIn(y_label))

        self.wait(0.5)

        # animate the move of the camera to properly see the axes
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=1.5)

        # built-in updater which begins camera rotation
        self.begin_ambient_camera_rotation(rate=0.15)

        cube = Cube(side_length=3, fill_opacity=0.5, stroke_width=2)

        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        self.wait(2)
        
        self.play(Write(cube))
        
        self.wait(4)
        
        for axis in [RIGHT, UP, OUT]:
            point1_coords = np.array(axis*5)
            point2_coords = np.array(-axis*5)
            line = Line3D(start=point1_coords, end=point2_coords, color=GREEN, stroke_width=3)
            self.play(Create(line))
            self.play(Rotate(cube, 4*PI/3, about_point=ORIGIN, axis=axis), run_time=3)
            self.play(FadeOut(line))
            
        
        self.wait(2)
        
        self.play(Unwrite(cube))

        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1) # Wait after fading outs
        
        
class EulerOrderPermutations(Scene):
    def construct(self):
        title = Tex(r"Permutations of X, Y, Z", color=YELLOW).scale(0.8)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Base letters at the top
        base_letters = VGroup(
            Tex("X", color=RED),
            Tex("Y", color=GREEN),
            Tex("Z", color=BLUE),
        ).arrange(RIGHT, buff=1).next_to(title, DOWN, buff=1)

        self.play(FadeIn(base_letters))
        self.wait(1)

        # Define the 2-letter permutations
        pair_perms = ["XY", "XZ", "YZ"]

        # Prepare Tex objects for pairs
        pair_texs = VGroup()
        colors = {"X": RED, "Y": GREEN, "Z": BLUE}

        for p in pair_perms:
            tex = Tex("".join(p)).scale(0.8)
            for i, ch in enumerate(p):
                tex[0][i].set_color(colors[ch])
            pair_texs.add(tex)

        pair_texs.arrange(RIGHT, buff=0.7).next_to(base_letters, DOWN, buff=1.5)


        # Animate copies of letters sliding down to form pairs
        
        for i, pair in enumerate(pair_perms):
            first_letter = pair[0]
            second_letter = pair[1]

            # Find the base letters matching these
            first_obj = next(m for m in base_letters if m.get_tex_string() == first_letter)
            second_obj = next(m for m in base_letters if m.get_tex_string() == second_letter)

            # Create copies that will slide down
            first_copy = first_obj.copy()
            second_copy = second_obj.copy()

            # Group them into a pair and move into position
            group = VGroup(first_copy, second_copy)

            self.play(TransformMatchingShapes(group, pair_texs[i]))

        self.wait(2)
        
        
        pair_perms2 = ["XY", "XZ", "YZ", "YZ", "XZ", "XY"]

        # Prepare Tex objects for pairs
        pair_texs2 = VGroup()
        colors = {"X": RED, "Y": GREEN, "Z": BLUE}

        for p in pair_perms2:
            tex = Tex("".join(p)).scale(0.8)
            for i, ch in enumerate(p):
                tex[0][i].set_color(colors[ch])
            pair_texs2.add(tex)

        pair_texs2.arrange(RIGHT, buff=0.7).next_to(base_letters, DOWN, buff=1.5)
        
        
        pair_texs_copy = pair_texs.copy()
        
        group = VGroup(pair_texs, pair_texs_copy)
        
        self.play(TransformMatchingShapes(group, pair_texs2))
        
        
        pair_perms3 = ["XY", "XZ", "YZ", "ZY", "ZX", "YX"]
        
        # Prepare Tex objects for pairs
        pair_texs3 = VGroup()
        colors = {"X": RED, "Y": GREEN, "Z": BLUE}

        for p in pair_perms3:
            tex = Tex("".join(p)).scale(0.8)
            for i, ch in enumerate(p):
                tex[0][i].set_color(colors[ch])
            pair_texs3.add(tex)

        pair_texs3.arrange(RIGHT, buff=0.7).next_to(base_letters, DOWN, buff=1.5)
        
        self.play(TransformMatchingShapes(pair_texs2, pair_texs3))
        
        row2 = pair_texs3.copy()
        
        row2_copy = row2.copy()
        
        row2.arrange(RIGHT, buff=0.7).next_to(pair_texs3, DOWN, buff=1.5)
        
        self.wait()
        
        self.play(TransformMatchingShapes(row2_copy, row2))
        
        
        row1_2 = ["XYX", "XZX", "YZY", "ZYZ", "ZXZ", "YXY"]
        
        # Prepare Tex objects for pairs
        _row1_2 = VGroup()
        colors = {"X": RED, "Y": GREEN, "Z": BLUE}

        for p in row1_2:
            tex = Tex("".join(p)).scale(0.8)
            for i, ch in enumerate(p):
                tex[0][i].set_color(colors[ch])
            _row1_2.add(tex)

        _row1_2.arrange(RIGHT, buff=0.7).next_to(base_letters, DOWN, buff=1.5)
        
        row2_2 = ["XYZ", "XZY", "YZX", "ZYX", "ZXY", "YXZ"]
        
        # Prepare Tex objects for pairs
        _row2_2 = VGroup()
        colors = {"X": RED, "Y": GREEN, "Z": BLUE}

        for p in row2_2:
            tex = Tex("".join(p)).scale(0.8)
            for i, ch in enumerate(p):
                tex[0][i].set_color(colors[ch])
            _row2_2.add(tex)

        _row2_2.arrange(RIGHT, buff=0.7).next_to(_row1_2, DOWN, buff=1.5)
        
        self.wait(5)
        
        self.play(TransformMatchingShapes(row2, _row2_2), TransformMatchingShapes(pair_texs3, _row1_2))
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1) # Wait after fading outs



class CompoundQuaternionDemo(Scene):
    def construct(self):
        # Title
        title = Tex("Compound Quaternion Rotations", font_size=48).to_edge(UP)
        self.add(title)

        # Step 1: Show the first rotation formula
        v_formula = MathTex(
            r"v' = q_1 \, v \, q_1^*", font_size=48
        ).next_to(title, DOWN, buff=1)
        self.play(Write(v_formula))
        self.wait(3)


        # Step 3: Introduce second rotation q2 on the outside
        q2_formula = MathTex(
            r"v'' = q_2 \left( q_1 \, v \, q_1^* \right) q_2^*", font_size=48
        ).move_to(v_formula.get_center())
        self.play(TransformMatchingShapes(v_formula, q2_formula), run_time=2)
        self.wait(1)
        
        # Step 6: Highlight the reason for multiplication order
        explanation = Tex(
            "Associativity of quaternions ensures the correct combined rotation",
            font_size=36
        ).next_to(q2_formula, DOWN, buff=1)
        self.play(FadeIn(explanation))
        self.wait(2)


        # Step 5: Show that we can group as (q2*q1) v (q2*q1)*
        final_formula = MathTex(
            r"v'' = (q_2 q_1) \, v \, (q_2 q_1)^*", font_size=48
        ).move_to(v_formula.get_center())
        self.play(TransformMatchingShapes(q2_formula, final_formula), run_time=2)
        self.wait(2)
 

        # Final note
        final_note = Tex(
            "Multiplying q2 * q1 combines rotations into a single quaternion",
            font_size=36
        ).next_to(explanation, DOWN, buff=1)
        self.play(FadeIn(final_note))
        self.wait(3)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1) # Wait after fading outs
        
        


class YXZQuaternionExpansion(Scene):
    def construct(self):
        title = Tex(r"$\text{YXZ Order Quaternion Expansion}$")
        self.play(title.animate.to_edge(UP))

        # Quaternion definitions (alphabetical) with selective coloring
        # assuming my_tex_template already defined and passed where needed
        qx = MathTex(
            r"q_x = \cos\!\left(\tfrac{\alpha}{2}\right) + \sin\!\left(\tfrac{\alpha}{2}\right) i_",
            substrings_to_isolate=["q_x", "i_"],
            tex_template=my_tex_template,
        ).next_to(title, DOWN)

        qx.set_color_by_tex("q_x", RED)
        qx.set_color_by_tex("i_", RED)

        qy = MathTex(
            r"q_y = \cos\!\left(\tfrac{\beta}{2}\right) + \sin\!\left(\tfrac{\beta}{2}\right) j_",
            substrings_to_isolate=["q_y", "j_"],
            tex_template=my_tex_template,
        ).next_to(qx, DOWN)

        qy.set_color_by_tex("q_y", GREEN)
        qy.set_color_by_tex("j_", GREEN)

        qz = MathTex(
            r"q_z = \cos\!\left(\tfrac{\gamma}{2}\right) + \sin\!\left(\tfrac{\gamma}{2}\right) k_",
            substrings_to_isolate=["q_z", "k_"],
            tex_template=my_tex_template,
        ).next_to(qy, DOWN)

        qz.set_color_by_tex("q_z", BLUE)
        qz.set_color_by_tex("k_", BLUE)



        self.play(*[Write(obj) for obj in [qx, qy, qz]])
        self.wait(1)

        # Full expanded quaternion in two columns
        quaternion_mult = MathTex(
            r"q * p = \\",
            r"(q_1 p_1 - q_2 p_2 - q_3 p_3 - q_4 p_4) \\"
            r"+ (q_1 p_2 + q_2 p_1 + q_3 p_4 - q_4 p_3) i \\",
            r"+ (q_1 p_3 - q_2 p_4 + q_3 p_1 + q_4 p_2) j \\"
            r"+ (q_1 p_4 + q_2 p_3 - q_3 p_2 + q_4 p_1) k \\",
            substrings_to_isolate=["i", "j", "k", "q_1", "q_2", "q_3", "q_4", "p_1", "p_2", "p_3", "p_4"],
            font_size=50
        ).scale(0.7).next_to(qz, DOWN, buff=1).shift(LEFT * 3.2)

        quaternion_mult.set_color_by_tex("i", RED)
        quaternion_mult.set_color_by_tex("j", GREEN)
        quaternion_mult.set_color_by_tex("k", BLUE)
        quaternion_mult.set_color_by_tex("q_1", ORANGE)
        quaternion_mult.set_color_by_tex("q_2", ORANGE)
        quaternion_mult.set_color_by_tex("q_3", ORANGE)
        quaternion_mult.set_color_by_tex("q_4", ORANGE)
        quaternion_mult.set_color_by_tex("p_1", YELLOW)
        quaternion_mult.set_color_by_tex("p_2", YELLOW)
        quaternion_mult.set_color_by_tex("p_3", YELLOW)
        quaternion_mult.set_color_by_tex("p_4", YELLOW)

        self.play(Write(quaternion_mult))
        self.wait(2)

        
        # Full expanded quaternion in two columns
        expanded2 = MathTex(
            r"q = & \,\,q_z q_x q_y \\",
            r"= & (\cos\!\tfrac{\alpha}{2}\cos\!\tfrac{\beta}{2}\cos\!\tfrac{\gamma}{2}"
            r"- \sin\!\tfrac{\alpha}{2}\sin\!\tfrac{\beta}{2}\sin\!\tfrac{\gamma}{2}) \,  \\",
            r"+ & (\sin\!\tfrac{\beta}{2}\cos\!\tfrac{\alpha}{2}\cos\!\tfrac{\gamma}{2} "
            r"- \sin\!\tfrac{\alpha}{2}\sin\!\tfrac{\gamma}{2}\cos\!\tfrac{\beta}{2}) \,i \\",
            r"+ & (\sin\!\tfrac{\alpha}{2}\cos\!\tfrac{\beta}{2}\cos\!\tfrac{\gamma}{2} "
            r"+ \sin\!\tfrac{\beta}{2}\sin\!\tfrac{\gamma}{2}\cos\!\tfrac{\alpha}{2}) \,j \\",
            r"+ & (\sin\!\tfrac{\alpha}{2}\sin\!\tfrac{\beta}{2}\cos\!\tfrac{\gamma}{2} "
            r"+ \cos\!\tfrac{\alpha}{2}\cos\!\tfrac{\beta}{2}\sin\!\tfrac{\gamma}{2}) \,k",
            substrings_to_isolate=["\,i", "\,j", "\,k", "q_x", "q_y", "q_z"],
            font_size=45,
        ).scale(0.7).next_to(qz, DOWN, buff=0.8).shift(RIGHT * 3.3)

        expanded2.set_color_by_tex("\,i", RED)
        expanded2.set_color_by_tex("\,j", GREEN)
        expanded2.set_color_by_tex("\,k", BLUE)
        expanded2.set_color_by_tex("q_x", RED)
        expanded2.set_color_by_tex("q_y", GREEN)
        expanded2.set_color_by_tex("q_z", BLUE)


        self.play(Write(expanded2))
        self.wait(2)
        
        list1 = [mob for mob in self.mobjects]
        list1.remove(expanded2)
        
        self.play(FadeOut(*list1))
        self.play(expanded2.animate.move_to(LEFT * 3))
        
        angle_assignments = MathTex(
            r"B_1 = &\cos\frac{\alpha}{2} \quad",
            r"A_1 = \sin\frac{\alpha}{2} \\\\",
            r"B_2 = &\cos\frac{\beta}{2} \quad",
            r"A_2 = \sin\frac{\beta}{2} \\\\",
            r"B_3 = &\cos\frac{\gamma}{2} \quad",
            r"A_3 = \sin\frac{\gamma}{2}",
            substrings_to_isolate=["B_1", "A_1", "B_2", "A_2", "B_3", "A_3"],
            font_size=45
        ).scale(0.7).next_to(expanded2, RIGHT, buff=2.4)
        
        angle_assignments.set_color_by_tex("B_1", RED)
        angle_assignments.set_color_by_tex("A_1", RED)
        angle_assignments.set_color_by_tex("B_2", GREEN)
        angle_assignments.set_color_by_tex("A_2", GREEN)
        angle_assignments.set_color_by_tex("B_3", BLUE)
        angle_assignments.set_color_by_tex("A_3", BLUE)

        self.play(Write(angle_assignments))
        self.wait(2)


        # Full expanded quaternion using variable assignments
        expanded_vars = MathTex(
            r"q = & q_z q_x q_y \\",
            r"= & (B_1 B_2 B_3 - A_1 A_2 A_3) \\",
            r"+ & (A_2 B_1 B_3 - A_1 A_3 B_2) \,i \\",
            r"+ & (A_1 B_2 B_3 + A_2 A_3 B_1) \,j \\",
            r"+ & (A_1 A_2 B_3 + A_3 B_1 B_2) \,k",
            substrings_to_isolate=["\,i", "\,j", "\,k", "q_x", "q_y", "q_z",
                                   "A_1","A_2","A_3","B_1","B_2","B_3"],
            font_size=45
        ).scale(0.7).move_to(expanded2)

        # Optional: color the variables for clarity
        expanded_vars.set_color_by_tex("\,i", RED)
        expanded_vars.set_color_by_tex("\,j", GREEN)
        expanded_vars.set_color_by_tex("\,k", BLUE)
        expanded_vars.set_color_by_tex("q_x", RED)
        expanded_vars.set_color_by_tex("q_y", GREEN)
        expanded_vars.set_color_by_tex("q_z", BLUE)
        expanded_vars.set_color_by_tex("A_1", RED)
        expanded_vars.set_color_by_tex("A_2", GREEN)
        expanded_vars.set_color_by_tex("A_3", BLUE)
        expanded_vars.set_color_by_tex("B_1", RED)
        expanded_vars.set_color_by_tex("B_2", GREEN)
        expanded_vars.set_color_by_tex("B_3", BLUE)

        self.play(TransformMatchingTex(expanded2, expanded_vars))
        self.wait(4)

        self.play(Circumscribe(angle_assignments))
        self.play(angle_assignments.animate.shift(RIGHT * 6))
        
        
        self.play(expanded_vars.animate.move_to(ORIGIN).scale(2))
    
        

        # Dictionary of Euler orders and their quaternion expressions
        euler_dict = {
            "XYZ": [
                r"  = & (B_1 B_2 B_3 + A_1 A_2 A_3) \\",
                r"  + & (A_1 B_2 B_3 - A_2 A_3 B_1) \,i \\",
                r"  + & (A_1 A_3 B_2 + A_2 B_1 B_3) \,j \\",
                r"  + & (A_3 B_1 B_2 - A_1 A_2 B_3) \,k"
            ],
            "ZYX": [
                r"  = & (B_1 B_2 B_3 - A_1 A_2 A_3) \\",
                r"  + & (A_1 A_2 B_3 + A_3 B_1 B_2) \,i \\",
                r"  + & (A_2 B_1 B_3 - A_1 A_3 B_2) \,j \\",
                r"  + & (A_1 B_2 B_3 + A_2 A_3 B_1) \,k"
            ],
            "YZX": [
                r"  = & (B_1 B_2 B_3 + A_1 A_2 A_3) \\",
                r"  + & (A_3 B_1 B_2 - A_1 A_2 B_3) \,i \\",
                r"  + & (A_1 B_2 B_3 - A_2 A_3 B_1) \,j \\",
                r"  + & (A_1 A_3 B_2 + A_2 B_1 B_3) \,k"
            ],
            "XZY": [
                r"  = & (B_1 B_2 B_3 - A_1 A_2 A_3) \\",
                r"  + & (A_1 B_2 B_3 + A_2 A_3 B_1) \,i \\",
                r"  + & (A_1 A_2 B_3 + A_3 B_1 B_2) \,j \\",
                r"  + & (A_2 B_1 B_3 - A_1 A_3 B_2) \,k"
            ],
            "YXZ": [
                r"  = & (B_1 B_2 B_3 - A_1 A_2 A_3) \\",
                r"  + & (A_2 B_1 B_3 - A_1 A_3 B_2) \,i \\",
                r"  + & (A_1 B_2 B_3 + A_2 A_3 B_1) \,j \\",
                r"  + & (A_1 A_2 B_3 + A_3 B_1 B_2) \,k"
            ],
            "ZXY": [
                r"  = & (B_1 B_2 B_3 + A_1 A_2 A_3) \\",
                r"  + & (A_1 A_3 B_2 + A_2 B_1 B_3) \,i \\",
                r"  + & (A_3 B_1 B_2 - A_1 A_2 B_3) \,j \\",
                r"  + & (A_1 B_2 B_3 - A_2 A_3 B_1) \,k"
            ],
            "ZYZ": [
                r"  = & (B_1 B_2 B_3 - A_1 A_3 B_2) \\",
                r"  + & (A_1 A_2 B_3 - A_2 A_3 B_1) \,i \\",
                r"  + & (A_1 A_2 A_3 + A_2 B_1 B_3) \,j \\",
                r"  + & (A_1 B_2 B_3 + A_3 B_1 B_2) \,k"
            ],
            "XYX": [
                r"  = & (B_1 B_2 B_3 - A_1 A_3 B_2) \\",
                r"  + & (A_1 B_2 B_3 + A_3 B_1 B_2) \,i \\",
                r"  + & (A_1 A_2 A_3 + A_2 B_1 B_3) \,j \\",
                r"  + & (A_2 A_3 B_1 - A_1 A_2 B_3) \,k"
            ],
            "YXY": [
                r"  = & (B_1 B_2 B_3 - A_1 A_3 B_2) \\",
                r"  + & (A_1 A_2 A_3 + A_2 B_1 B_3) \,i \\",
                r"  + & (A_1 B_2 B_3 + A_3 B_1 B_2) \,j \\",
                r"  + & (A_1 A_2 B_3 - A_2 A_3 B_1) \,k"
            ],
            "XZX": [
                r"  = & (B_1 B_2 B_3 - A_1 A_3 B_2) \\",
                r"  + & (A_1 B_2 B_3 + A_3 B_1 B_2) \,i \\",
                r"  + & (A_1 A_2 B_3 - A_2 A_3 B_1) \,j \\",
                r"  + & (A_1 A_2 A_3 + A_2 B_1 B_3) \,k"
            ],
            "ZXZ": [
                r"  = & (B_1 B_2 B_3 - A_1 A_3 B_2) \\",
                r"  + & (A_1 A_2 A_3 + A_2 B_1 B_3) \,i \\",
                r"  + & (A_2 A_3 B_1 - A_1 A_2 B_3) \,j \\",
                r"  + & (A_1 B_2 B_3 + A_3 B_1 B_2) \,k"
            ],
            "YZY": [
                r"  = & (B_1 B_2 B_3 - A_1 A_3 B_2) \\",
                r"  + & (A_2 A_3 B_1 - A_1 A_2 B_3) \,i \\",
                r"  + & (A_1 B_2 B_3 + A_3 B_1 B_2) \,j \\",
                r"  + & (A_1 A_2 A_3 + A_2 B_1 B_3) \,k"
            ],
        }

        # Animate through each order
        n = 0
        for order, expr_lines in euler_dict.items():
            next_tex = MathTex(rf"q = & q_{{{order[2].lower()}}} q_{{{order[1].lower()}}} q_{{{order[0].lower()}}} \\", *expr_lines, substrings_to_isolate=["\,i", "\,j", "\,k", "q_{x}", "q_{y}", "q_{z}", "A_1","A_2","A_3","B_1","B_2","B_3"], font_size=45).scale(0.7).scale(2).move_to(ORIGIN)
            # Apply coloring
            next_tex.set_color_by_tex("\,i", RED)
            next_tex.set_color_by_tex("\,j", GREEN)
            next_tex.set_color_by_tex("\,k", BLUE)
            next_tex.set_color_by_tex("q_{x}", RED)
            next_tex.set_color_by_tex("q_{y}", GREEN)
            next_tex.set_color_by_tex("q_{z}", BLUE)
            next_tex.set_color_by_tex("A_1", RED)
            next_tex.set_color_by_tex("A_2", GREEN)
            next_tex.set_color_by_tex("A_3", BLUE)
            next_tex.set_color_by_tex("B_1", RED)
            next_tex.set_color_by_tex("B_2", GREEN)
            next_tex.set_color_by_tex("B_3", BLUE)

            # Update title
            if n == 0:
                title = Tex(f"Euler Order: {order}", font_size=36).move_to(title.get_center())
            else:
                new_title = Tex(f"Euler Order: {order}", font_size=36).move_to(title.get_center())
            
            self.play(
                TransformMatchingTex(expanded_vars, next_tex),
                (Transform(title, new_title) if n == 1 else FadeIn(title)),
                run_time=1
            )
            self.wait(1)
            expanded_vars = next_tex
            n = 1

        self.wait(2)

        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1) # Wait after fading outs


# --- New Scene: Slerp Coefficients Plot ---
class SlerpCoefficientsPlot(Scene):

    def construct(self):
        # Animate theta from 0.01° to 180°
        theta_tracker = ValueTracker(np.deg2rad(0.01))


        # --- Dynamic axes and plot lines ---
        def get_ymax(theta):
            # Avoid division by zero for theta near 0
            if np.isclose(np.sin(theta), 0):
                return 1.1
            t_vals = np.linspace(0, 1, 200)
            s0 = np.abs(np.sin((1 - t_vals) * theta) / np.sin(theta))
            s1 = np.abs(np.sin(t_vals * theta) / np.sin(theta))
            max_val = np.max([s0, s1])
            return max(1.1, max_val * 1.1)


        def get_scene():
            theta = theta_tracker.get_value()
            y_max = get_ymax(theta)
            axes = Axes(
                x_range=[0, 1, 0.2],
                y_range=[0, y_max, 0.2],
                axis_config={"color": WHITE},
                x_length=7,
                y_length=4,
            )
            axes.add_coordinates()
            x_label = axes.get_x_axis_label(Tex("t", font_size=28))
            y_label = axes.get_y_axis_label(Tex(r"$s_n$", font_size=28))
            legend = VGroup(
                Line(color=BLUE).set_stroke(width=6).set_length(0.5),
                Tex(r"$s_0 = \frac{\sin((1-t)\theta)}{\sin\theta}$", color=BLUE, font_size=28),
                Line(color=YELLOW).set_stroke(width=6).set_length(0.5),
                Tex(r"$s_1 = \frac{\sin(t\theta)}{\sin\theta}$", color=YELLOW, font_size=28),
            ).arrange(RIGHT, buff=0.3).next_to(axes, UP)
            title = Tex(
                r"Slerp Coefficients for $\theta = {:.0f}^\circ$".format(np.rad2deg(theta)),
                font_size=36
            ).next_to(legend, UP)
            def s0_func(t):
                if np.isclose(np.sin(theta), 0):
                    return 1.0
                return np.sin((1-t)*theta)/np.sin(theta)
            def s1_func(t):
                if np.isclose(np.sin(theta), 0):
                    return 0.0
                return np.sin(t*theta)/np.sin(theta)
            s0_graph = axes.plot(s0_func, color=BLUE, x_range=[0,1]).set_clip_path(axes)
            s1_graph = axes.plot(s1_func, color=YELLOW, x_range=[0,1]).set_clip_path(axes)
            return VGroup(axes, x_label, y_label, legend, title, s0_graph, s1_graph)

        scene_group = always_redraw(get_scene)
        self.add(scene_group)
        self.wait(0.5)
        self.play(theta_tracker.animate.set_value(np.deg2rad(179.9)), run_time=5, rate_func=smooth)



# --- New Scene: Vector Chain Demo ---
class VectorChainDemo(Scene):
    def construct(self):
        # Define vectors
        v1 = np.array([2, 1, 0])
        v2 = np.array([-1.7, -1, 0])
        n1 = 10
        n2 = 10

        # Start at origin
        points = [np.array([0, 0, 0])]
        # Add 10 of v1
        for _ in range(n1):
            points.append(points[-1] + v1)
        # Add 10 of v2
        for _ in range(n2):
            points.append(points[-1] + v2)

        # Draw the chain
        chain = VGroup()

        for i in range(1, len(points)):
            seg = Arrow(start=points[i-1], end=points[i], buff=0, stroke_width=6, color=BLUE if i <= n1 else YELLOW)
            chain.add(seg)

        # Dots at each joint
        dots = VGroup(*[Dot(point=pt, radius=0.07, color=WHITE) for pt in points])

        
        # Center everything
        group = VGroup(chain, dots).move_to(ORIGIN)

        self.play(Create(chain), FadeIn(dots), run_time=10)
        self.wait(0.5)

