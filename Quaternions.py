from manim import *
from math import atan, sin, cos, sqrt
import numpy as np



# Custom LaTeX template with colors
my_tex_template = TexTemplate()
my_tex_template.add_to_preamble(r"\usepackage{xcolor}")
my_tex_template.add_to_preamble(r"\usepackage[usenames,dvipsnames]{xcolor}")
my_tex_template.add_to_preamble(r"\usepackage[HTML]{xcolor}")
my_tex_template.add_to_preamble(r"\definecolor{vibrantpurple}{HTML}{9B30FF}")
my_tex_template.add_to_preamble(r"\definecolor{brightblue}{HTML}{1E90FF}")



class Rotations2D(MovingCameraScene):
    def construct(self):
        
        axes = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            x_length=20,
            y_length=20,
            axis_config={
                "include_numbers": False,
            }
        )
         
        self.add(axes)
        axes.set_opacity(0)

        square = Square(fill_opacity=0.75, color=GREEN).scale(2).shift(RIGHT * 1.5)

        self.play(Write(square))
        self.wait(2)
        
        dot = Dot().shift(RIGHT * 1.5)
        self.play(Write(dot))
        self.wait()
        self.play(Rotate(square, 60 * DEGREES))
        self.wait()
        self.play(Unwrite(dot))
        self.wait(2)
        
        dot = Dot()
        self.play(Write(dot))
        self.wait()
        self.play(Rotate(square, -160 * DEGREES, about_point=ORIGIN))
        self.wait()
        self.play(Unwrite(dot))
        self.wait(4)
        
        self.play(
            axes.animate.set_opacity(100),
            self.camera.auto_zoom(axes),
            )
        
        self.play(FocusOn(ORIGIN))
        
        
        dot = Dot().shift(RIGHT * 5 + UP * 3)
        dot.set_opacity(0)
        self.add(dot)
        
        arrow = Arrow(start=ORIGIN, end=dot, color=YELLOW, buff=0)
        self.play(Write(arrow))
        
        arrow.add_updater(lambda m: m.become(Arrow(ORIGIN, dot, color=YELLOW, buff=0)))

            
        
        arc = Arc(
            radius=2,
            start_angle=0,
            angle=atan(3/5),
            stroke_color=YELLOW,
            stroke_width=6
        ).move_arc_center_to(ORIGIN)
        
        def update_func(mob: Arc):
            mob.angle = atan(dot.get_y()/dot.get_x())
            if mob.angle < 0:
                mob.stroke_color = RED
            mob.generate_points()
        
        
        arc0 = Arc(
            radius=2,
            start_angle=0,
            angle=atan(3/5),
            stroke_color=RED,
            stroke_width=6
        ).move_arc_center_to(ORIGIN)
        arc0.set_opacity(0)
        self.add(arc0)
        
        self.play(Write(arc))
        arc0.set_opacity(100)
        
        # Animate the arrow rotating clockwise by, for example, 90 degrees
        self.play(
            Rotate(dot, angle=-PI/1.7, about_point=ORIGIN),
            UpdateFromFunc(arc, update_func),
            run_time=2,
            )
        
        arrow.clear_updaters()
        arc.clear_updaters()
        
        self.play(Unwrite(arrow),
                  Unwrite(arc),
                  Unwrite(arc0),
                  )
        
        
        dot = Dot().shift(RIGHT * 5 + UP * 3)
        self.play(Write(dot))
        self.play(
            Rotate(dot, angle=-PI/1.7, about_point=ORIGIN),
            run_time=2,
            )
        
        self.wait()
        self.play(Unwrite(dot))
        self.play(Unwrite(square))
        self.wait()
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1) # Wait after fading outs
        
        
        
        
class Rotations3D(ThreeDScene):
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
        self.wait(2)
        
        for axis in [RIGHT, UP, OUT]:
            self.play(Rotate(cube, PI / 2, about_point=ORIGIN, axis=axis), run_time=1.5)
        
        self.wait(4)
        
        for axis in [RIGHT + UP, UP + LEFT, OUT + DOWN + RIGHT]:
            point1_coords = np.array(axis*3)
            point2_coords = np.array(-axis*3)
            line = Line3D(start=point1_coords, end=point2_coords, color=GREEN)
            self.play(Create(line))
            self.play(Rotate(cube, PI, about_point=ORIGIN, axis=axis), run_time=3)
            self.play(FadeOut(line))
            
        
        self.wait(2)
        
        self.play(Unwrite(cube))

        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1) # Wait after fading outs
        
        


class SqrtMinusOneIsWhat(Scene):
    def construct(self):
        # Create the text object with larger font size
        equation_text = MathTex(r"\sqrt{-1} = ?", font_size=144)
        
        # Fade in the text
        self.play(FadeIn(equation_text))
        self.wait(2)  # Keep it on screen for 2 seconds
        # Fade out the text
        self.play(FadeOut(equation_text))
        self.wait(1)
        
        
        
        
class OffTheNumberLineIsWhat(Scene):
    def complex_to_point(self, c):
        # Assuming the complex plane maps real to x and imaginary to y
        return self.axes.c2p(c.real, c.imag)

    def construct(self):
        # Create axes to base the scene on
        self.axes = Axes(
            x_range=[-10, 10, 1],
            x_length=10,
            y_range=[-10, 10, 1],
            y_length=10,
            axis_config={"include_numbers": True}
        )
        
        # Create a number line from -10 to 10
        number_line = NumberLine(
            x_range=[-10, 10, 1],
            length=10,
            include_numbers=True,
        )
        for number in number_line.numbers:
            number.font_size = 24

        # Add arrows indicating extension to infinity
        left_arrow = Arrow(
            start=number_line.get_start(),
            end=number_line.get_start() + LEFT * 0.5,
            buff=0
        )
        right_arrow = Arrow(
            start=number_line.get_end(),
            end=number_line.get_end() + RIGHT * 0.5,
            buff=0
        )

        # Add number line to scene
        self.play(Create(number_line))
        self.play(GrowArrow(left_arrow), GrowArrow(right_arrow))
        self.wait()
        
        
        
        # Create a dot at number 6
        dot = Dot(color=YELLOW, radius=0.1).move_to(number_line.number_to_point(6))
        label = Text("6").scale(0.5).next_to(dot, UP, buff=0.3)

        # Create a semi-transparent circle for glow effect
        glow_circle = Circle(radius=0.15, color=YELLOW, fill_opacity=0.2).move_to(dot)

        # Add dot to scene
        self.play(FadeIn(glow_circle), FadeIn(dot), FadeIn(label))
        

        # Move dot from 6 to -2
        target_position = number_line.number_to_point(-2)
        target_label = Text("-2").scale(0.5).next_to(target_position, UP, buff=0.3)

        self.play(
            dot.animate.move_to(target_position),
            glow_circle.animate.move_to(target_position),
            Transform(label, target_label),
            run_time=2
        )
        
        
        # Move dot from -2 to 4
        target_position = number_line.number_to_point(4)
        target_label = Text("4").scale(0.5).next_to(target_position, UP, buff=0.3)

        self.play(
            dot.animate.move_to(target_position),
            glow_circle.animate.move_to(target_position),
            Transform(label, target_label),
            run_time=2
        )
        
        self.wait(2)
        
        
        # Move the dot to a complex number
        target_position = self.complex_to_point(3 + 2j)  # Convert complex to scene point
        target_label = Text("??").scale(0.5).next_to(target_position, UP, buff=0.3)


        # Animate the dot moving to the complex number position
        self.play(
            dot.animate.move_to(target_position),
            glow_circle.animate.move_to(target_position),
            Transform(label, target_label),
            run_time=2
        )
        
        self.wait(2)
        
        self.play(
            FadeOut(dot),
            FadeOut(label),
            FadeOut(number_line),
            FadeOut(left_arrow),
            FadeOut(right_arrow),
            FadeOut(glow_circle),
            )
        
        
        
        
class SquareRootsIntro(Scene):
    def complex_to_point(self, c):
        # Assuming the complex plane maps real to x and imaginary to y
        return self.axes.c2p(c.real, c.imag)

    def construct(self):
        # Create axes to base the scene on
        self.axes = Axes(
            x_range=[-10, 10, 1],
            x_length=10,
            y_range=[-10, 10, 1],
            y_length=10,
            axis_config={"include_numbers": True}
        )
        
        # Create a number line from -10 to 10
        number_line = NumberLine(
            x_range=[-10, 10, 1],
            length=10,
            include_numbers=True,
        )
        for number in number_line.numbers:
            number.font_size = 24

        # Add arrows indicating extension to infinity
        left_arrow = Arrow(
            start=number_line.get_start(),
            end=number_line.get_start() + LEFT * 0.5,
            buff=0
        )
        right_arrow = Arrow(
            start=number_line.get_end(),
            end=number_line.get_end() + RIGHT * 0.5,
            buff=0
        )

        # Add number line to scene
        self.play(Create(number_line))
        self.play(GrowArrow(left_arrow), GrowArrow(right_arrow))
        self.wait()
        
        
        
        # Create a dot at number 9
        dot = Dot(color=YELLOW, radius=0.1).move_to(number_line.number_to_point(9))
        label = Text("9").scale(0.5).next_to(number_line.number_to_point(9), UP, buff=0.3)

        # Create a semi-transparent circle for glow effect
        glow_circle = Circle(radius=0.15, color=YELLOW, fill_opacity=0.2).move_to(dot)

        # Add dot to scene
        self.play(FadeIn(glow_circle), FadeIn(dot), FadeIn(label))
        
        
        
        # Create the first part of the equation
        equation = MathTex(r"\sqrt{9} = ?", font_size=144)
        equation.to_edge(UP, buff=1)


        # Animate the equation
        self.play(FadeIn(equation))
        self.wait(2)
        
        answer = MathTex(r"\sqrt{9} = 3", font_size=144)
        answer.to_edge(UP, buff=1)
        
        # New 9 dot 
        dot0 = Dot(color=BLUE, radius=0.1).move_to(number_line.number_to_point(9))
        label0 = Text("9").scale(0.5).next_to(number_line.number_to_point(9), UP, buff=0.3)

        # Create a semi-transparent circle for glow effect
        glow_circle0 = Circle(radius=0.15, color=BLUE, fill_opacity=0.2).move_to(dot0)
        
        
        target_position = number_line.number_to_point(3)
        target_label = Text("3").scale(0.5).next_to(target_position, UP, buff=0.3)
        
        self.play(
            FadeIn(glow_circle0),
            FadeIn(dot0),
            FadeIn(label0),
            Transform(equation, answer),
            dot.animate.move_to(target_position),
            glow_circle.animate.move_to(target_position),
            Transform(label, target_label),
            )
        
        self.wait(2)
        
        # re-arrange equation
        equation2 = MathTex(r"3 * 3 = 9", font_size=144)
        equation2.to_edge(UP, buff=1)
        
        # Animate the equation
        self.play(
            FadeOut(equation),
            Transform(answer, equation2),
            )
           
        # Shrink and move up
        answer.set_opacity(0)
        self.play(
            equation2.animate.scale(0.5),
        )
        self.play(
            equation2.animate.move_to(UP * 3),
        )
        
        self.wait(2)
        
        # Negative root
        copy_equation = equation2.copy()
        
        equation3 = MathTex(r"-3 * -3 = 9", font_size=72)
        equation3.to_edge(UP, buff=1)
        
        self.play(
            FadeIn(copy_equation),
            copy_equation.animate.move_to(UP * 2),
        )
        
        equation3.move_to(copy_equation)
        self.play(
            Transform(copy_equation, equation3),
        )
        
        # Copy dot to -3
        dot2 = Dot(color=YELLOW, radius=0.1).move_to(number_line.number_to_point(3))
        label2 = Text("3").scale(0.5).next_to(dot2, UP, buff=0.3)

        # Create a semi-transparent circle for glow effect
        glow_circle2 = Circle(radius=0.15, color=YELLOW, fill_opacity=0.2).move_to(dot2)

        target_position = number_line.number_to_point(-3)
        target_label = Text("-3").scale(0.5).next_to(target_position, UP, buff=0.3)

        # Add dot to scene
        self.play(
            FadeIn(glow_circle2),
            FadeIn(dot2),
            FadeIn(label2),
            dot.animate.move_to(target_position),
            glow_circle.animate.move_to(target_position),
            Transform(label, target_label),
            )
        
        
        self.wait(2)
        
        
        # Fade out equations
        self.play(
            FadeOut(equation2),
            FadeOut(equation3),
            FadeOut(copy_equation),
            )
        
        self.wait(2)
        
        # Define the pivot point
        pivot = ORIGIN

        # Create the main line starting from the pivot
        line = Line(pivot, self.complex_to_point(9))
        line.set_color(BLUE)

        # Create a dot at the end of the line
        end_dot = Dot(color=BLUE)
        end_dot.move_to(line.get_end())

        # Add the line and dot to the scene
        self.add(line, end_dot)

        # Update the dot position as the line rotates
        def updater(mob):
            mob.move_to(line.get_end())

        end_dot.add_updater(updater)
        

        self.wait()

        # Angle of points
        angle_text1 = MathTex(r"\theta = 0^{\circ}", font_size=36)
        angle_text1.move_to(self.complex_to_point(9 + 2j))
        
        angle_text2 = MathTex(r"\theta = 360^{\circ}", font_size=36)
        angle_text2.move_to(self.complex_to_point(9 + 3j))
        
        angle_text3 = MathTex(r"\theta = 720^{\circ}", font_size=36)
        angle_text3.move_to(self.complex_to_point(9 + 4j))
        
        angle_text4 = MathTex(r"...", font_size=36)
        angle_text4.move_to(self.complex_to_point(9 + 5j))
        
        for i in range(1, 5):
            self.play(
                FadeIn(eval(f"angle_text{i}")),
                Rotating(line, angle=2 * PI, about_point=pivot),
                run_time=3,
                rate_func=smooth
                )
            
            self.wait(1)
            
        self.play(
            FadeOut(line),
            FadeOut(end_dot),
            )
        
        self.wait(2)

        halfangle_text1 = MathTex(r"\theta/2 = 0^{\circ}", font_size=36)
        halfangle_text1.move_to(self.complex_to_point(3 + 2j))
        
        halfangle_text2 = MathTex(r"\theta/2 = 180^{\circ}", font_size=36)
        halfangle_text2.move_to(self.complex_to_point(-3 + 3j))
        
        halfangle_text3 = MathTex(r"\theta/2 = 360^{\circ}", font_size=36)
        halfangle_text3.move_to(self.complex_to_point(3 + 4j))
        
        halfangle_text4 = MathTex(r"...", font_size=36)
        halfangle_text4.move_to(self.complex_to_point(-3 + 5j))
        
        
        self.play(
                Transform(angle_text1, halfangle_text1),
                Transform(angle_text2, halfangle_text2),
                Transform(angle_text3, halfangle_text3),
                Transform(angle_text4, halfangle_text4),
                )
        
        self.wait(1)
        
        
        self.play(
            halfangle_text1.animate.move_to(self.complex_to_point(3 + 2j)),
            halfangle_text2.animate.move_to(self.complex_to_point(-3 + 2j)),
            halfangle_text3.animate.move_to(self.complex_to_point(3 + 2j)),
            halfangle_text4.animate.move_to(self.complex_to_point(-3 + 2j)),
            FadeOut(halfangle_text3),
            FadeOut(halfangle_text4),
            FadeOut(angle_text1),
            FadeOut(angle_text2),
            FadeOut(angle_text3),
            FadeOut(angle_text4),
            )
        
        self.wait(5)
        
        self.play(
            FadeOut(dot0),
            FadeOut(dot),
            FadeOut(dot2),
            FadeOut(glow_circle0),
            FadeOut(glow_circle),
            FadeOut(glow_circle2),
            FadeOut(label0),
            FadeOut(label),
            FadeOut(label2),
            FadeOut(halfangle_text1),
            FadeOut(halfangle_text2),
            )
        
        
        
class NegativeSquareRoots(Scene):
    def complex_to_point(self, c):
        # Assuming the complex plane maps real to x and imaginary to y
        return self.axes.c2p(c.real, c.imag)

    def construct(self):
        # Create axes to base the scene on
        self.axes = Axes(
            x_range=[-10, 10, 1],
            x_length=10,
            y_range=[-10, 10, 1],
            y_length=10,
            axis_config={"include_numbers": True,
                         "include_tip": False}
        )
        for number in self.axes.get_x_axis().numbers:
            number.font_size = 24

        # Set font size for y-axis tick labels
        for number in self.axes.get_y_axis().numbers:
            number.font_size = 24
            number.shift(RIGHT * 0.1)
        
        # Create a number line from -10 to 10
        number_line = NumberLine(
            x_range=[-10, 10, 1],
            length=10,
            include_numbers=True,
        )
        for number in number_line.numbers:
            number.font_size = 24

        # Add arrows indicating extension to infinity
        left_arrow = Arrow(
            start=number_line.get_start(),
            end=number_line.get_start() + LEFT * 0.5,
            buff=0
        )
        right_arrow = Arrow(
            start=number_line.get_end(),
            end=number_line.get_end() + RIGHT * 0.5,
            buff=0
        )

        # Add number line to scene
        self.add(number_line, left_arrow, right_arrow)
        self.wait()
        
        
        
        # Create a dot at minus 9
        dot = Dot(color=BLUE, radius=0.1).move_to(number_line.number_to_point(-9))
        label = Text("-9").scale(0.5).next_to(number_line.number_to_point(-9), UP, buff=0.3)

        # Create a semi-transparent circle for glow effect
        glow_circle = Circle(radius=0.15, color=BLUE, fill_opacity=0.2).move_to(dot)

        # Add dot to scene
        self.play(FadeIn(glow_circle), FadeIn(dot), FadeIn(label))
        
        # Create the first part of the equation
        equation = MathTex(r"\sqrt{-9} = ?", font_size=144)
        equation.to_edge(UP, buff=1)


        # Animate the equation
        self.play(FadeIn(equation))
        self.wait(2)
        self.play(FadeOut(equation))
        self.wait(2)
        
        # Define the pivot point
        pivot = ORIGIN

        # Create the main line starting from the pivot
        line = Line(pivot, self.complex_to_point(9))
        line.set_color(BLUE)

        # Create a dot at the end of the line
        end_dot = Dot(color=BLUE)
        end_dot.move_to(line.get_end())

        # Add the line and dot to the scene
        self.add(line, end_dot)

        # Update the dot position as the line rotates
        def updater(mob):
            mob.move_to(line.get_end())

        end_dot.add_updater(updater)

        
        angle_text1 = MathTex(r"\theta = 180^{\circ}", font_size=36)
        angle_text1.move_to(self.complex_to_point(-9 + 2j))
        
        angle_text2 = MathTex(r"\theta = 540^{\circ}", font_size=36)
        angle_text2.move_to(self.complex_to_point(-9 + 3j))
        
        angle_text3 = MathTex(r"\theta = 900^{\circ}", font_size=36)
        angle_text3.move_to(self.complex_to_point(-9 + 4j))
        
        angle_text4 = MathTex(r"...", font_size=36)
        angle_text4.move_to(self.complex_to_point(-9 + 5j))
        
        self.play(
                Rotate(line, angle=PI, about_point=pivot),
                run_time=3,
                rate_func=smooth
                )
        self.wait(1)
        for i in range(1, 5):
            self.play(
                FadeIn(eval(f"angle_text{i}")),
                Rotate(line, angle=2 * PI, about_point=pivot),
                run_time=3,
                rate_func=smooth
                )
            
            self.wait(1)
        
        self.play(FadeOut(line), FadeOut(end_dot))
        self.wait(2)
        
        
        halfangle_text1 = MathTex(r"\theta/2 = 90^{\circ}", font_size=36)
        halfangle_text1.move_to(self.complex_to_point(6 + 2j))
        
        halfangle_text2 = MathTex(r"\theta/2 = 270^{\circ}", font_size=36)
        halfangle_text2.move_to(self.complex_to_point(6 + -3j))
        
        halfangle_text3 = MathTex(r"\theta/2 = 450^{\circ}", font_size=36)
        halfangle_text3.move_to(self.complex_to_point(6 + 4j))
        
        halfangle_text4 = MathTex(r"...", font_size=36)
        halfangle_text4.move_to(self.complex_to_point(6 + -5j))
        
        
        self.play(
                Transform(angle_text1, halfangle_text1),
                Transform(angle_text2, halfangle_text2),
                Transform(angle_text3, halfangle_text3),
                Transform(angle_text4, halfangle_text4),
                )
        
        self.wait(3)
        
        
        self.play(
            halfangle_text1.animate.move_to(self.complex_to_point(6 + 3j)),
            halfangle_text2.animate.move_to(self.complex_to_point(6 + -3j)),
            halfangle_text3.animate.move_to(self.complex_to_point(6 + 3j)),
            halfangle_text4.animate.move_to(self.complex_to_point(6 + -3j)),
            FadeOut(halfangle_text3),
            FadeOut(halfangle_text4),
            FadeOut(angle_text1),
            FadeOut(angle_text2),
            FadeOut(angle_text3),
            FadeOut(angle_text4),
            )
        
        self.wait(2)
        
        
        

        # Create the main line starting from the pivot
        line = Line(ORIGIN, self.complex_to_point(3))
        line.set_color(YELLOW)

        # Create a dot at the end of the line
        end_dot = Dot(color=YELLOW)
        end_dot.move_to(line.get_end())

        # Add the line and dot to the scene
        self.play(FadeIn(line), FadeIn(end_dot))

        # Update the dot position as the line rotates
        def updater(mob):
            mob.move_to(line.get_end())

        end_dot.add_updater(updater)
        

        # Create the arc at the pivot point
        quarter_arc = Arc(
            radius=0.75,
            start_angle=0,
            angle=PI/2,
            stroke_color=YELLOW,
            stroke_width=2
        )
        quarter_arc.move_arc_center_to(ORIGIN)
        
        half_arc = Arc(
            radius=0.75,
            start_angle=PI/2,
            angle=PI,
            stroke_color=YELLOW,
            stroke_width=2
        )
        half_arc.move_arc_center_to(ORIGIN)
        
        plus_i = MathTex(r"90^{\circ}", font_size=36)
        plus_i.move_to(self.complex_to_point(6 + 3j))
        
        minus_i = MathTex(r"270^{\circ}", font_size=36)
        minus_i.move_to(self.complex_to_point(6 - 3j))
        
        dot3i = Dot(color=YELLOW, radius=0.1).move_to(self.complex_to_point(3j))
        label3i = Text("??").scale(0.5).next_to(self.complex_to_point(3j), RIGHT, buff=0.3)

        # Create a semi-transparent circle for glow effect
        glow_circle3i = Circle(radius=0.15, color=YELLOW, fill_opacity=0.2).move_to(dot3i)
        
        dotneg3i = Dot(color=YELLOW, radius=0.1).move_to(self.complex_to_point(-3j))
        labelneg3i = Text("??").scale(0.5).next_to(self.complex_to_point(-3j), RIGHT, buff=0.3)

        # Create a semi-transparent circle for glow effect
        glow_circleneg3i = Circle(radius=0.15, color=YELLOW, fill_opacity=0.2).move_to(dotneg3i)

        
        # Show the points 3i and -3i from angle
        self.play(
            Create(quarter_arc),
            Rotate(line, angle=PI/2, about_point=ORIGIN),
            run_time=3,
            rate_func=smooth,
            )

        self.play(
            Transform(halfangle_text1, plus_i),
            FadeIn(glow_circle3i),
            FadeIn(dot3i),
            FadeIn(label3i),
            )
        
        self.play(
            Create(half_arc),
            Rotate(line, angle=PI, about_point=ORIGIN),
            run_time=3,
            rate_func=smooth,
            )
        
        self.play(
            Transform(halfangle_text2, minus_i),
            FadeIn(glow_circleneg3i),
            FadeIn(dotneg3i),
            FadeIn(labelneg3i),
            )
        
        self.play(
            FadeOut(line),
            FadeOut(end_dot),
            FadeOut(quarter_arc),
            FadeOut(half_arc),
            FadeOut(plus_i),
            FadeOut(minus_i),
            FadeOut(halfangle_text1),
            FadeOut(halfangle_text2),
            )
        
        self.wait(5)
        
        self.play(
            Create(self.axes),
            FadeOut(number_line),
            )
        
        self.wait(2)
        
        Real = Text("Real").next_to(number_line.number_to_point(10), UP, buff=0.3)
        Imaginary = Text("Imaginary").next_to(self.complex_to_point(6j), RIGHT, buff=0.5)
        
        self.play(
            FadeIn(Real),
            FadeIn(Imaginary),
            )
        
        self.wait(5)
        
        Re = Text("Re").next_to(number_line.number_to_point(10), UP, buff=0.3)
        Im = Text("Im").next_to(self.complex_to_point(6j), RIGHT, buff=0.5)
        
        self.play(
            Transform(Real, Re),
            Transform(Imaginary, Im),
            )
        
        self.wait(5)
        
        
        newlabel3i = Text("3i").scale(0.5).next_to(self.complex_to_point(3j), RIGHT, buff=0.3)
        newlabelneg3i = Text("-3i").scale(0.5).next_to(self.complex_to_point(-3j), RIGHT, buff=0.3)
        
        
        self.play(
            Transform(label3i, newlabel3i),
            Transform(labelneg3i, newlabelneg3i),
            )
        
        self.wait(5)
        
        self.play(
            FadeOut(self.axes),
            FadeOut(labelneg3i),
            FadeOut(label3i),
            FadeOut(dot3i),
            FadeOut(dotneg3i),
            FadeOut(glow_circle3i),
            FadeOut(glow_circleneg3i),
            FadeOut(left_arrow),
            FadeOut(right_arrow),
            FadeOut(dot),
            FadeOut(label),
            FadeOut(glow_circle),
            FadeOut(Re),
            FadeOut(Im),
            FadeOut(Real),
            FadeOut(Imaginary),
            )



class ImaginaryUnitRevealed(Scene):
    def construct(self):
        # Create the text object with larger font size
        equation_text = MathTex(r"\sqrt{-9} = 3i", font_size=144)
        equation_text2 = MathTex(r"\sqrt{-1} = i", font_size=144)
        
        # Fade in the text
        self.play(FadeIn(equation_text))
        self.wait(2)
        
        # Transform /3
        self.play(Transform(equation_text, equation_text2))
        self.wait(2)
        
        # Fade out the text
        self.play(FadeOut(equation_text), FadeOut(equation_text2))
        self.wait(1)



class ComplexIntroAndAdditionSubtraction(Scene):
    def construct(self):
        # Create axes for the complex plane
        axes1 = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=7,
            y_length=7,
            axis_config={
                "include_numbers": True,
                "numbers_to_include": np.arange(-4, 5, 1),
            }
        )
        
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=7,
            y_length=7,
            axis_config={
                "include_numbers": False,
            }
        )

        # Add axis labels
        axes_labels = axes1.get_axis_labels(x_label="Re", y_label="Im")
        self.play(Create(axes1), Write(axes_labels))
        self.wait(2)
        
        self.play(FadeIn(axes), FadeOut(axes1))
        
        self.wait(2)
        
        grid = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=7,
            y_length=7,
            background_line_style={
                "stroke_color": GREY,
                "stroke_opacity": 0.5
            }
        )
        self.play(Create(grid))
        
                
        self.wait(2)        

        # Add some example complex numbers as points
        points = [
            (1, 2),    # 1 + 2i
            (-2, -1),  # -2 - i
            (0, -3),   # -3i
            (2.5, 0),  # 2.5
            (-2, 2),   # -2 + 2i
        ]
        
        n = 0
        dots = []
        for re, im in points:
            point = axes.c2p(re, im)
            dot = Dot(point, color=RED)
            dots.append(dot)
            exec(f"label{n} = MathTex(f\"{re}{'+' if im >= 0 else ''}{im}i\", color=BLUE).next_to(point, UP)")
            self.play(FadeIn(dot), Write(eval(f"label{n}")))
            self.wait(0.5)
            n += 1

        self.wait(2)

        # Fade out all
        self.play(FadeOut(VGroup(axes, axes_labels, grid)))
        
        self.wait(2)
        
        n = 0
        labels2 = []
        for re, im in points:
            point = axes.c2p(re, im)
            # Assuming re, im, n, dot are defined
            exec(f"label2{n} = MathTex(r\"\\begin{{bmatrix}} {re} \\\\ {im} \\end{{bmatrix}}\", color=BLUE).next_to(point, UP)")
            labels2.append(eval(f"label{n}"))
            exec(f"self.play(Transform(label{n}, label2{n}))")
            exec(f"label{n}.opacity = 0")
            n += 1
            
        # Animate drawing vectors (arrows) from origin to these points
        arrows = []
        for re, im in points:
            start = axes.c2p(0, 0)
            end = axes.c2p(re, im)
            arrows.append(Arrow(start=start, end=end, buff=0, color=YELLOW, stroke_width=2, tip_length=0.2))
        self.play((Create(arrow) for arrow in arrows), run_time=1)
        self.wait(1)
            
        n = 0
        labels = []
        for re, im in points:
            point = axes.c2p(re, im)
            labels.append(MathTex(f"{re}{'+' if im >= 0 else ''}{im}i", color=BLUE).next_to(point, UP))
            n += 1
            
        self.play((Transform(label2, label) for (label2, label) in zip(labels2, labels)))
        
        self.play(
            (FadeOut(dot) for dot in dots),
            FadeIn(grid),
            run_time=2,
            )
            
        self.play(
            labels2[2].animate.next_to(axes.c2p(2.5, -3), DOWN),
            arrows[2].animate.move_to(axes.c2p(2.5, -1.5)),
            )
         
        self.wait(1)
        
        combine = VGroup(labels2[2], labels2[3])
        
        addition = MathTex(f"(2.5 + 0i) + (0 - 3i)", color=BLUE).next_to(axes.c2p(2.5, -3), DOWN)
        
        self.play(
            labels2[3].animate.next_to(axes.c2p(1.5, -3), DOWN),
            labels2[2].animate.next_to(axes.c2p(3.5, -3), DOWN),
            Transform(combine, addition),
                  )
        
        sum_ = MathTex(f"2.5 - 3i", color=BLUE).next_to(axes.c2p(2.5, -3), DOWN)
        self.wait(2)
        self.play(
            Transform(combine, sum_),
                  )
        
        self.wait(2)
        
        self.play(
            FadeOut(labels2[3]),
            FadeOut(labels2[2]),
            FadeOut(arrows[3]),
            FadeOut(arrows[2]),
            )
        
        self.wait(2)
        
        self.play(
            labels2[4].animate.next_to(axes.c2p(0, -3), DOWN),
            arrows[4].animate.move_to(axes.c2p(-1, -2)),
            )
        
        self.wait(2)
        
        combine = VGroup(labels2[1], labels2[4])
        
        addition = MathTex(f"(-2 - 1i) - (-2 + 2i)", color=BLUE).next_to(axes.c2p(0, -3), DOWN)
        
        self.play(
            labels2[1].animate.next_to(axes.c2p(1.5, -3), DOWN),
            labels2[4].animate.next_to(axes.c2p(-1.5, -3), DOWN),
            Transform(combine, addition),
                  )
                               
        sum_ = MathTex(f"0 - 3i", color=BLUE).next_to(axes.c2p(0, -3), DOWN)
        self.wait(2)
        self.play(
            Transform(combine, sum_),
                  )
        
        self.wait(2)
        
        self.play(
            FadeOut(labels2[1]),
            FadeOut(labels2[4]),
            FadeOut(arrows[1]),
            FadeOut(arrows[4]),
            FadeOut(labels2[0]),
            FadeOut(arrows[0]),
            )
        
        self.wait(2)  




class ComplexMultiplicationIntro(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=7,
            y_length=7,
            axis_config={
                "include_numbers": False,
            }
        )
        grid = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=7,
            y_length=7,
            background_line_style={
                "stroke_color": GREY,
                "stroke_opacity": 0.5
            }
        )

        # Add axes, labels, and grid to the scene
        self.add(axes, grid)
        axes.set_opacity(0)
        self.wait(2)

        # Define two complex points (for example, 1 + 2i and 2 + i)
        re1, im1 = -1, 2
        re2, im2 = 2, 1

        # Convert to Manim points
        point1 = axes.c2p(re1, im1)
        point2 = axes.c2p(re2, im2)

        # Create dots for the points
        dot1 = Dot(point1, color=RED)
        dot2 = Dot(point2, color=GREEN)

        # Add the dots
        self.play(Create(dot1), Create(dot2))
        self.wait(1)

        # Draw vectors (arrows) from origin to the points
        arrow1 = Arrow(start=axes.c2p(0, 0), end=point1, buff=0, color=RED, tip_length=0.2)
        arrow2 = Arrow(start=axes.c2p(0, 0), end=point2, buff=0, color=GREEN, tip_length=0.2)
        self.play(Create(arrow1), Create(arrow2))
        self.wait(1)

        # Calculate the product of the two complex numbers
        re_product = re1 * re2 - im1 * im2
        im_product = re1 * im2 + re2 * im1
        product_point = axes.c2p(re_product, im_product)

        # Create a dot for the product
        product_dot = Dot(product_point, color=BLUE)
        product_label = MathTex(f"{re1}{'+' if im1 >=0 else ''}{im1}i \\times {re2}{'+' if im2 >=0 else ''}{im2}i = {re_product}{'+' if im_product >=0 else ''}{im_product}i")
        product_label.next_to(product_dot, UP)

        # Animate the product point and label
        self.play(FadeIn(product_dot), Write(product_label))
        self.wait(2)

        # Optionally, animate the vector for the product
        product_arrow = Arrow(start=axes.c2p(0, 0), end=product_point, buff=0, color=YELLOW)
        self.play(Create(product_arrow))
        self.wait(2)
        
        arcgreen = Arc(
            radius=0.75,
            start_angle=0,
            angle=atan(0.5),
            stroke_color=GREEN,
            stroke_width=3
        ).move_arc_center_to(ORIGIN)
        
        arcred = Arc(
            radius=1,
            start_angle=0,
            angle=atan(0.5)+PI/2,
            stroke_color=RED,
            stroke_width=3
        ).move_arc_center_to(ORIGIN)
        
        self.play(Create(arcgreen))
        self.play(Create(arcred))
        
        self.play(
            arcgreen.animate.set_stroke(width=5),
            arcred.animate.set_stroke(width=5),
        )
        
        self.wait(1)
        
        self.play(arcred.animate.rotate(atan(0.5)))
        self.play(arcred.animate.move_arc_center_to(ORIGIN))
        
        arcred2 = Arc(
            radius=0.75,
            start_angle=atan(0.5),
            angle=atan(0.5)+PI/2,
            stroke_color=RED,
            stroke_width=5
        ).move_arc_center_to(ORIGIN)
        
        self.play(Transform(arcred, arcred2))
        
        arcblue = Arc(
            radius=0.75,
            start_angle=0,
            angle=atan(0.5)*2+PI/2,
            stroke_color=BLUE,
            stroke_width=5
        ).move_arc_center_to(ORIGIN)
        
        self.play(Create(arcblue))
        self.wait(5)
        
        self.play(Write(MathTex("|\mathbf{v}| = |\mathbf{a}| * |\mathbf{b}|").next_to(axes.c2p(-5.5, 2), DOWN)))
        
        self.wait(5)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1) # Wait after fading outs



class ComplexRotations2D(MovingCameraScene):
    def construct(self):
        axes = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            x_length=20,
            y_length=20,
            axis_config={
                "include_numbers": False,
            }
        )
         
        self.add(axes)
        axes.set_opacity(0)

        
        self.play(
            axes.animate.set_opacity(100),
            self.camera.auto_zoom(axes),
            )
        
        
        
        dot1 = Dot().shift(RIGHT * 5)
        self.play(Write(dot1))
        self.play(Indicate(dot1))
        
        arrow1 = Arrow(start=ORIGIN, end=dot1, color=YELLOW, buff=0)
        label1 = MathTex(r"\vec{a}", font_size=70).next_to(arrow1, DOWN)
        self.play(Write(arrow1), Write(label1))
        
        arrow1.add_updater(lambda m: m.become(Arrow(ORIGIN, dot1, color=YELLOW, buff=0)))
        label1.add_updater(lambda m: m.become(MathTex(r"\vec{a}", font_size=70).next_to(arrow1, DOWN)))
        
        self.wait(2)
        
        dot2 = Dot().shift(RIGHT * sqrt(2)/2 + UP * sqrt(2)/2)
        self.play(Write(dot2))
        self.play(Indicate(dot2))
        
        arrow2 = Arrow(start=ORIGIN, end=dot2, color=GREEN, buff=0)
        label2 = MathTex(r"\vec{m}", font_size=70).next_to(arrow2, LEFT)
        self.play(Write(arrow2), Write(label2))
        
        arrow2.add_updater(lambda m: m.become(Arrow(ORIGIN, dot2, color=GREEN, buff=0)))
        label2.add_updater(lambda m: m.become(MathTex(r"\vec{m}", font_size=70).next_to(arrow2, LEFT)))
        
        
        magnitudes = MathTex(r"|\vec{p}| = |\vec{a}| * |\vec{m}|", font_size=90).next_to(axes.c2p(-5, 3), LEFT)
        
        self.play(Write(magnitudes))
        
        angles = MathTex(r"\angle{\vec{p}} = \angle{\vec{a}} + \angle{\vec{m}}", font_size=90).next_to(axes.c2p(-4.4, 1), LEFT)
        
        self.play(Write(angles))
        
        self.wait(4)
        
        magnitudes2 = MathTex(r"|\vec{p}| = 5 * 1", font_size=90).next_to(axes.c2p(-5, 3), LEFT)
        
        self.play(Transform(magnitudes, magnitudes2))
        
        angles2 = MathTex(r"\angle{\vec{p}} = 0^{\circ} + 45^{\circ}", font_size=90).next_to(axes.c2p(-4.4, 1), LEFT)
        
        self.play(Transform(angles, angles2))
        
        self.wait(3)
        
        dot3 = Dot([dot1.get_x() * dot2.get_x() - dot1.get_y() * dot2.get_y(), dot1.get_x() * dot2.get_y() + dot2.get_x() * dot1.get_y(), 0])
        self.play(Write(dot3))
        self.play(Indicate(dot3))
        
        dot3.add_updater(lambda m: m.become(Dot([dot1.get_x() * dot2.get_x() - dot1.get_y() * dot2.get_y(), dot1.get_x() * dot2.get_y() + dot2.get_x() * dot1.get_y(), 0], color=YELLOW)))

        
        arrow3 = Arrow(start=ORIGIN, end=dot3, color=RED, buff=0)
        label3 = MathTex(r"\vec{p}", font_size=70).next_to(arrow3, UP)
        self.play(Write(arrow3), Write(label3))
        
        arrow3.add_updater(lambda m: m.become(Arrow(ORIGIN, dot3, color=RED, buff=0)))
        label3.add_updater(lambda m: m.become(MathTex(r"\vec{p}", font_size=70).next_to(arrow3, UP)))
        
        self.wait(2)
        
        angles3 = MathTex(r"\angle{\vec{p}} = \angle{\vec{a}} + \angle{\vec{m}}", font_size=90).next_to(axes.c2p(-4.4, 1), LEFT)
        magnitudes3 = MathTex(r"|\vec{p}| = |\vec{a}| * |\vec{m}|", font_size=90).next_to(axes.c2p(-5, 3), LEFT)
        
        self.play(Transform(angles, angles3), Transform(magnitudes, magnitudes3))
        
        self.wait(2)
        
        self.play(Rotate(dot1, angle=-PI/3, about_point=ORIGIN))
        self.wait()
        self.play(Rotate(dot2, angle=PI/4, about_point=ORIGIN))
        self.play(Rotate(dot2, angle=3*PI/4, about_point=ORIGIN))
        self.wait()
        self.play(Rotate(dot1, angle=2*PI-0.2, about_point=ORIGIN), run_time=4)
        self.wait(5)
        
        for mobject in self.mobjects:
            mobject.clear_updaters()
        
        self.play(
            FadeOut(magnitudes),
            FadeOut(angles),
            FadeOut(dot3),
            FadeOut(arrow3),
            FadeOut(label3),
            FadeOut(dot1),
            FadeOut(arrow1),
            FadeOut(label1),
            )
        
        circle0 = Circle(radius=1.5)
        circle = Circle(radius=1, stroke_width=1)
        
        self.play(
            self.camera.auto_zoom(circle0),
            )
        
        self.play(Write(circle))
        
        self.wait(5)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1) # Wait after fading outs
        


class EulersFormula(MovingCameraScene):
    def construct(self):
        # Draw the axes and the unit circle
        axes = Axes(
            x_range=[-1.5, 1.5],
            y_range=[-1.5, 1.5],
            x_length=8,
            y_length=8,
            axis_config={"include_numbers": False}
        )

        circle = Circle(radius=1, color=WHITE)
        circle0 = Circle(radius=2, color=WHITE)
        self.play(Create(axes), Create(circle))
        self.play(self.camera.auto_zoom(circle0))
        self.wait()
        
        theta = 45 * DEGREES
        
        dot = Dot([np.cos(theta), np.sin(theta), 0], radius=0.04)
        
        
        arrow = Arrow(ORIGIN, [np.cos(theta), np.sin(theta), 0], buff=0, color=YELLOW, stroke_width=2, tip_length=0.1)
      
        self.play(Create(arrow))
        arrow.add_updater(lambda m: m.become(Arrow(ORIGIN, [dot.get_x(), dot.get_y(), 0], color=YELLOW, buff=0, stroke_width=2, tip_length=0.1)))

        
        def update_func(mob: Arc):
            mob.angle = atan(abs(dot.get_y())/abs(dot.get_x()))
            if dot.get_x() < 0:
                if dot.get_y() < 0:
                    mob.angle += 180 * DEGREES
                else:
                    mob.angle = 180 * DEGREES - mob.angle
            else:
                if dot.get_y() < 0:
                    mob.angle = 360 * DEGREES - mob.angle
                else:
                    pass
            mob.generate_points()
            
        
        
        # Draw an arc representing θ
        arc = Arc(radius=0.5, start_angle=0, angle=theta, color=YELLOW, stroke_width=1)
        self.play(Create(arc))
        self.wait()

        # Label for θ
        theta_label = MathTex(r"\theta", font_size=30).next_to(arc, RIGHT, buff=0.1)
        self.play(Write(theta_label))
        self.wait()
        
        
        self.play(
            Rotate(dot, angle=PI, about_point=ORIGIN),
            UpdateFromFunc(arc, update_func),
            )

        self.wait(1)
        
        self.play(Unwrite(axes))
        
        self.wait(1)

        # Draw the projection lines for cosine and sine
        line_cos = DashedLine(
            start=ORIGIN,
            end=[dot.get_x(), 0, 0],
            color=BLUE,
            stroke_width=2
        )
        line_cos.add_updater(lambda m: m.become(DashedLine(
            start=ORIGIN,
            end=[dot.get_x(), 0, 0],
            color=BLUE,
            stroke_width=2
        )))

        line_sin = DashedLine(
            start=[dot.get_x(), 0, 0],
            end=[dot.get_x(), dot.get_y(), 0],
            color=GREEN,
            stroke_width=2
        )
        line_sin.add_updater(lambda m: m.become(DashedLine(
            start=[dot.get_x(), 0, 0],
            end=[dot.get_x(), dot.get_y(), 0],
            color=GREEN,
            stroke_width=2
        )))
        self.play(Create(line_cos), Create(line_sin))
        self.wait()
    

        # Label for cosine and sine
        cos_label = MathTex(r"\cos \theta", font_size=22, color=BLUE).move_to(line_cos)
        cos_label.add_updater(lambda m: m.become(MathTex(r"\cos \theta", font_size=22, color=BLUE).move_to(line_cos)))
        sin_label = MathTex(r"\sin \theta", font_size=22, color=GREEN).move_to(line_sin)
        sin_label.add_updater(lambda m: m.become(MathTex(r"\sin \theta", font_size=22, color=GREEN).move_to(line_sin)))
        self.play(Write(cos_label), Write(sin_label))
        self.wait(5)
        
        self.play(
            Rotate(dot, angle=5*PI/2, about_point=ORIGIN),
            UpdateFromFunc(arc, update_func),
            run_time=5,
            )

        # Show the complex exponential representation
        exp_eq = MathTex(r"e^{i\theta} = \cos \theta + i \sin \theta")
        exp_eq.move_to(DOWN * 1.5)
        self.play(Write(exp_eq))
        self.wait()



        # Show the corresponding complex exponential (as a vector)
        
        label_exp = MathTex(r"e^{i\theta}", font_size=22).next_to(dot, RIGHT*0.2)
        label_exp.add_updater(lambda m: m.become(MathTex(r"e^{i\theta}", font_size=22).next_to(dot, RIGHT*0.2)))
        self.play(Write(label_exp))
        self.wait()
        
        self.play(
            Rotate(dot, angle=-2*PI, about_point=ORIGIN),
            UpdateFromFunc(arc, update_func),
            run_time=5,
            )
        
        title = Text('Euler\'s Formula').move_to(UP*1.5)
        self.play(Write(title), run_time=3)
        self.wait(3)
        
        self.play(Unwrite(title), Unwrite(cos_label), Unwrite(sin_label))
        
        circle0 = Circle(radius=2, color=WHITE).shift(RIGHT + DOWN * 0.2)
        self.play(self.camera.auto_zoom(circle0))
        
        self.wait()
        
        cos_label = MathTex(rf"\cos \theta = {dot.get_x():.2f}", font_size=22, color=BLUE).move_to(RIGHT*2.5 + UP * 0.2)
        cos_label.add_updater(lambda m: m.become(MathTex(rf"\cos \theta = {dot.get_x():.2f}", font_size=22, color=BLUE).move_to(RIGHT*2.5 + UP * 0.2)))
        sin_label = MathTex(rf"\sin \theta = {dot.get_y():.2f}", font_size=22, color=GREEN).move_to(RIGHT*2.5 + DOWN * 0.2)
        sin_label.add_updater(lambda m: m.become(MathTex(rf"\sin \theta = {dot.get_y():.2f}", font_size=22, color=GREEN).move_to(RIGHT*2.5 + DOWN * 0.2)))
        self.play(Write(cos_label), Write(sin_label))
        
        self.play(
            Rotate(dot, angle=2*PI, about_point=ORIGIN),
            UpdateFromFunc(arc, update_func),
            run_time=10,
            )
        self.wait()
        
        for mobject in self.mobjects:
            mobject.clear_updaters()
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1) # Wait after fading outs
        
        
        
class EulersFormulaForQuaternions(Scene):
    def construct(self):
        # Main formula
        formula = MathTex(r"e^{i\theta} = \cos \theta + i \sin \theta", font_size=90)
        self.play(Write(formula))
        self.wait(1)

        # Second formula with bold u
        formula2 = MathTex(r"e^{\mathbf{u}\theta} = \cos \theta + \mathbf{u} \sin \theta", font_size=90)

        # Animate transition
        self.play(Transform(formula, formula2))
        self.wait(3)

        # Fade out the final formula
        self.play(Unwrite(formula))
        self.wait(1)
        
        
        
class QuaternionsStructure(MovingCameraScene):
    def construct(self):
        _complex = MathTex(r"a + b\textit{i}", font_size=300)
        self.play(Write(_complex))
        self.wait(4)
        
        _quaternion = MathTex(r"a + b\textit{i} + c\textit{j} + d\textit{k}", font_size=300)
        bigger = MathTex(r"a + b\textit{i} + c\textit{j} + d\textit{k}", font_size=350)
        
        self.play(Transform(_complex, _quaternion), self.camera.auto_zoom(bigger))
        
        self.wait(5)
        
        _vector = MathTex(r"a + \vec{v}", font_size=300)
        
        self.play(Transform(_complex, _vector))
        
        self.wait(5)
        
        _vector2 = MathTex(r"(a, \vec{v})", font_size=300)
        
        self.play(Transform(_complex, _vector2))
        
        self.wait(5)
        
        formula = MathTex(r"e^{\mathbf{u}\theta} = \cos \theta + \mathbf{u} \sin \theta", font_size=200).shift(UP*4)
        
        self.play(Write(formula))
        self.wait(2)
        
        formula2 = MathTex(r"e^{\mathbf{u}\theta} = \cos \theta + (b\textit{i} + c\textit{j} + d\textit{k}) \sin \theta", font_size=100).shift(UP*4)
        bigger = MathTex(r"e^{\mathbf{u}\theta} = \cos \theta + (b\textit{i} + c\textit{j} + d\textit{k}) \sin \theta", font_size=150).shift(UP*4)
        
        self.play(self.camera.auto_zoom(bigger), Unwrite(_complex))
        self.wait()
        self.play(TransformMatchingShapes(formula, formula2))
        self.wait()
        self.play(TransformMatchingShapes(formula2, formula))
        
        exp = MathTex(r"\mathbf{q} = e^{\mathbf{u}\theta}", font_size=200).shift(UP*4)
        
        self.wait(2)
        
        self.play(TransformMatchingShapes(formula, exp))
        
        self.wait()
        
        q = MathTex(r"\mathbf{q}", font_size=200).shift(UP*4)
        
        self.play(TransformMatchingShapes(exp, q))
        
        self.wait(2)
        
        self.play(Unwrite(q))
        self.wait()



class ComplexRotationsSquare(MovingCameraScene):
    def construct(self):
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=10,
            axis_config={"color": WHITE},
        )

        x_label = axes.get_x_axis_label(Tex("x"))
        y_label = axes.get_y_axis_label(Tex("y"))
        
        self.add(axes)

        
        self.play(
            axes.animate.set_opacity(100),
            self.camera.auto_zoom(axes),
            FadeIn(axes), FadeIn(x_label), FadeIn(y_label)
            )
        

        # Complex multiplication
        def complex_multiply(z1, z2):
            x1, y1 = z1
            x2, y2 = z2
            return (x1 * x2 - y1 * y2, x1 * y2 + y1 * x2)

        theta = ValueTracker(0)

        def rotator():
            return (cos(theta.get_value()), sin(theta.get_value()))

        dot_colors = [RED, BLUE, GREEN, ORANGE]

        # Initial square vertices
        base_points = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

        # Create dots with updaters
        dots = []
        for i, pt in enumerate(base_points):
            dot = Dot(color=dot_colors[i]).add_updater(
                lambda m, pt=pt: m.move_to(
                    axes.c2p(*complex_multiply(pt, rotator()))
                )
            )
            dots.append(dot)

        self.play(*[Write(dot) for dot in dots])

        # Connect edges
        lines = []
        for i in range(len(dots)):
            line = Line().add_updater(
                lambda m, i=i: m.become(
                    Line(dots[i].get_center(), dots[(i + 1) % len(dots)].get_center(), color=WHITE)
                )
            )
            lines.append(line)
            self.add(line)

        self.play(*[Create(line) for line in lines])

        # LaTeX showing multiplication rule
        text = MathTex(
            r"p = (\pm 1 \pm i) * q", font_size=100, tex_template=my_tex_template
        ).to_corner(UL).shift(LEFT*2 + UP)
        self.play(Write(text))

                # Dynamic LaTeX for e^{iθ}
        exp_text = MathTex(
            r"q = e^{i\theta} = "
            + f"{cos(theta.get_value()):.2f} "
            + ("+" if sin(theta.get_value()) >= 0 else "-")
            + rf"\textcolor{{brightblue}}{{{abs(sin(theta.get_value())):.2f}}}\textcolor{{brightblue}}{{i}}",
            font_size=100,
            tex_template=my_tex_template,
        ).to_edge(DOWN).shift(DOWN)

        self.play(Write(exp_text))

        exp_text.add_updater(
            lambda m: m.become(
                MathTex(
                    r"q = e^{i\theta} = "
                    + f"{cos(theta.get_value()):.2f} "
                    + ("+" if sin(theta.get_value()) >= 0 else "-")
                    + rf"\textcolor{{brightblue}}{{{abs(sin(theta.get_value())):.2f}}}\textcolor{{brightblue}}{{i}}",
                    font_size=100,
                    tex_template=my_tex_template,
                ).to_edge(DOWN).shift(DOWN)
            )
        )

        # θ label
        theta_text = MathTex(r"\theta = ", font_size=100, tex_template=my_tex_template).to_corner(UR).shift(LEFT*2 + UP)
        label = DecimalNumber(theta.get_value(), unit=r"^\circ", num_decimal_places=2, font_size=100).next_to(theta_text, RIGHT)
        self.play(Create(theta_text), Create(label))

        label.add_updater(lambda m: m.set_value(theta.get_value() / DEGREES))


        # Animate rotation
        self.play(
            theta.animate.increment_value(360 * DEGREES),
            run_time=10,
            rate_func=rate_functions.ease_in_out_sine,
        )

        # Trails
        trails = [
            TracedPath(dot.get_center, stroke_color=dot.get_color(), stroke_width=2, dissipating_time=0)
            for dot in dots
        ]
        for trail in trails:
            self.add(trail)

        self.play(
            theta.animate.increment_value(-360 * DEGREES),
            run_time=10,
            rate_func=rate_functions.ease_in_out_sine,
        )

        self.wait(2)

        # Cleanup
        for m in self.mobjects:
            m.clear_updaters()
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)
        
        
        
class QuaternionRotations3D(ThreeDScene):
    def construct(self):
        
        def quaternion_multiply(q1, q2, w=False):
            """
            Multiply two quaternions.
            q1 and q2 are tuples or lists: (w, x, y, z)
            Returns: (w, x, y, z)
            """
            w1, x1, y1, z1 = q1
            w2, x2, y2, z2 = q2

            _w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
            x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
            y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
            z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
            
            if w:
                return (_w, x, y, z)
            else:
                return (x, y, z)
            
            
        def normalize(v):
            v = np.array(v, dtype=float)
            norm = np.linalg.norm(v)
            if norm == 0:
                return v
            return v / norm

        
        def get_axis():
            return normalize(axis_dot.get_center())
        
        def q(dash):
            return (cos(theta.get_value()), *(get_axis()[i] * sin(theta.get_value()) * [-1, 1][dash == 0] for i in range(3)))
        
        def live_pos(dot):
            dot.update()
            return dot.get_center()
        
        def connect(dot_a, dot_b, color=GREY):
            return Line(color=color).add_updater(
                lambda m: m.put_start_and_end_on(live_pos(dot_a), live_pos(dot_b))
            )
        
        
        axes = ThreeDAxes()

        x_label = axes.get_x_axis_label(Tex("x"))
        y_label = axes.get_y_axis_label(Tex("y")).shift(UP * 1.8)

        # zoom out so we see the axes
        self.set_camera_orientation(zoom=0.5)

        self.play(FadeIn(axes), FadeIn(x_label), FadeIn(y_label))

        # animate the move of the camera to properly see the axes
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=1.5)

        # built-in updater which begins camera rotation
        self.begin_ambient_camera_rotation(rate=0.15)

        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        
        axis = normalize(np.array([1, 1, 1]))
        theta = ValueTracker(0)
        
        axis_dot = Dot3D(axis)
        axis_dot.set_opacity(0)
        self.add(axis_dot)
        
        
        line = Line3D(
            start=-3 * get_axis(),
            end=3 * get_axis(),
            color=GREEN,
            thickness=0.04,
        )
        
        def axis_update(line):
            line.become(Line3D(
            start=-3 * get_axis(),
            end=3 * get_axis(),
            color=GREEN,
            thickness=0.04,
        ))
            
        line.add_updater(axis_update)
        #self.add_updater(lambda dt: print("q:", q(0)))

        
        
        self.add(line)
        line.set_opacity(0)
        
        
        
        dot_colors = [RED, BLUE, GREEN, YELLOW, ORANGE, PURPLE, TEAL, PINK]


        dot1 = Dot3D(color=dot_colors[0]).add_updater(lambda m: m.move_to(quaternion_multiply([0, 1, 1, 1], q(dash=0))))
        dot2 = Dot3D(color=dot_colors[1]).add_updater(lambda m: m.move_to(quaternion_multiply([0, 1, 1, -1], q(dash=0))))
        dot3 = Dot3D(color=dot_colors[2]).add_updater(lambda m: m.move_to(quaternion_multiply([0, 1, -1, 1], q(dash=0))))
        dot4 = Dot3D(color=dot_colors[3]).add_updater(lambda m: m.move_to(quaternion_multiply([0, 1, -1, -1], q(dash=0))))
        dot5 = Dot3D(color=dot_colors[4]).add_updater(lambda m: m.move_to(quaternion_multiply([0, -1, 1, 1], q(dash=0))))
        dot6 = Dot3D(color=dot_colors[5]).add_updater(lambda m: m.move_to(quaternion_multiply([0, -1, 1, -1], q(dash=0))))
        dot7 = Dot3D(color=dot_colors[6]).add_updater(lambda m: m.move_to(quaternion_multiply([0, -1, -1, 1], q(dash=0))))
        dot8 = Dot3D(color=dot_colors[7]).add_updater(lambda m: m.move_to(quaternion_multiply([0, -1, -1, -1], q(dash=0))))
        
            
        
        dots = [dot1, dot2, dot3, dot4, dot5, dot6, dot7, dot8]

        for d in dots:
            d.update(0)
        
        
        line1  = connect(dot1, dot2)
        line2  = connect(dot4, dot3)
        line3  = connect(dot1, dot3)
        line4  = connect(dot2, dot4)
        line5  = connect(dot5, dot6)
        line6  = connect(dot8, dot7)
        line7  = connect(dot5, dot7)
        line8  = connect(dot6, dot8)
        line9  = connect(dot1, dot5)
        line10 = connect(dot2, dot6)
        line11 = connect(dot3, dot7)
        line12 = connect(dot4, dot8)
        
        lines = [line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11, line12]
        
        self.add(*dots)
        self.add(*lines)
        
        self.play(Write(VGroup(*dots, *lines)))
        

        # Define faces using dot indices
        faces = [
            [0, 1, 3, 2],  # Front
            [4, 5, 7, 6],  # Back
            [0, 1, 5, 4],  # Top
            [2, 3, 7, 6],  # Bottom
            [0, 2, 6, 4],  # Left
            [1, 3, 7, 5],  # Right
        ]

        # Colors for each face
        face_colors = [RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE]

        # Create and add polygon faces with updaters
        cube_faces = []
        for i, face_indices in enumerate(faces):
            color = face_colors[i]
            # Initial polygon
            face = Polygon(
                *[dots[j].get_center() for j in face_indices],
                color=color,
                fill_color=color,
                stroke_opacity=0.8,
                fill_opacity=0.8,
                sheen_direction=UL,
                shade_in_3d=True
            )

            def updater(m, face_indices=face_indices):
                # Update vertices directly, no need to rebuild Polygon
                new_points = [dots[j].get_center() for j in face_indices]
                m.set_points_as_corners(new_points + [new_points[0]])  # close polygon

            face.add_updater(updater)
            cube_faces.append(face)
            self.add(face)

        # One-liner to play all creations
        self.play(Create(VGroup(*cube_faces)))


        # Adding the LaTeX texts
        text = MathTex(
            r"p_1 = (0, \pm 1, \pm 1, \pm 1) * q",
            font_size=50
        ).move_to(LEFT * 4 + UP * 3)
        self.add_fixed_in_frame_mobjects(text)
        self.play(Write(text))
        

        self.wait(2)
        
        
        # Build all parts first (with their own updaters)
        prefix = MathTex(r"q = e^{\mathbf{u} \theta} = ", font_size=50)

        # --- w_sign ---
        w_sign = MathTex("+", font_size=50)
        w_val = DecimalNumber(abs(cos(theta.get_value())), num_decimal_places=2, font_size=50)

        # --- x_sign ---
        x_sign = MathTex("+", font_size=50)
        x_val = DecimalNumber(abs(get_axis()[0] * sin(theta.get_value())), num_decimal_places=2, font_size=50, color="#FF3333")
        x_unit = MathTex(r"\boldsymbol{i}", font_size=50, color="#FF3333")

        # --- y_sign ---
        y_sign = MathTex("+", font_size=50)
        y_val = DecimalNumber(abs(get_axis()[1] * sin(theta.get_value())), num_decimal_places=2, font_size=50, color="#9B30FF")  
        y_unit = MathTex(r"\boldsymbol{j}", font_size=50, color="#9B30FF")

        # --- z_sign ---
        z_sign = MathTex("+", font_size=50)
        z_val = DecimalNumber(abs(get_axis()[2] * sin(theta.get_value())), num_decimal_places=2, font_size=50, color="#1E90FF")
        z_unit = MathTex(r"\boldsymbol{k}", font_size=50, color="#1E90FF")

        # --- group ---
        text4 = VGroup(prefix, w_sign, w_val,
                       x_sign, x_val, x_unit,
                       y_sign, y_val, y_unit,
                       z_sign, z_val, z_unit)

        text4.add_updater(lambda m: m.arrange(RIGHT, buff=0.1).move_to(DOWN * 3.5))

        # Lock to screen
        self.add_fixed_in_frame_mobjects(text4)
        self.play(Write(text4))

        w_val.add_updater(lambda m: m.set_value(abs(cos(theta.get_value()))))
        x_val.add_updater(lambda m: m.set_value(abs(get_axis()[0] * sin(theta.get_value()))))
        y_val.add_updater(lambda m: m.set_value(abs(get_axis()[1] * sin(theta.get_value()))))
        z_val.add_updater(lambda m: m.set_value(abs(get_axis()[2] * sin(theta.get_value()))))
        w_val.add_updater(lambda m: self.add_fixed_in_frame_mobjects(m))
        x_val.add_updater(lambda m: self.add_fixed_in_frame_mobjects(m))
        y_val.add_updater(lambda m: self.add_fixed_in_frame_mobjects(m))
        z_val.add_updater(lambda m: self.add_fixed_in_frame_mobjects(m))
        
        w_sign.add_updater(lambda m: m.become(MathTex("+" if cos(theta.get_value()) >= 0 else "-", font_size=50).move_to(m)))
        x_sign.add_updater(lambda m: m.become(MathTex("+" if get_axis()[0] * sin(theta.get_value()) >= 0 else "-", font_size=50).move_to(m)))
        y_sign.add_updater(lambda m: m.become(MathTex("+" if get_axis()[1] * sin(theta.get_value()) >= 0 else "-", font_size=50).move_to(m)))
        z_sign.add_updater(lambda m: m.become(MathTex("+" if get_axis()[2] * sin(theta.get_value()) >= 0 else "-", font_size=50).move_to(m)))




        self.wait(1)

        # Create the initial MathTex object
        theta_text = MathTex(r"\theta = ", font_size=50).move_to(LEFT * 6.1 + UP * 2)
        self.add_fixed_in_frame_mobjects(theta_text)

        # Create DecimalNumber to display theta's value
        label = DecimalNumber(theta.get_value(), unit=r"^\circ", num_decimal_places=2).move_to(LEFT * 5 + UP * 2)
        self.add_fixed_in_frame_mobjects(label)
        self.play(Create(theta_text), Create(label))

        # Add updater to label to keep it synced with theta
        label.add_updater(
            lambda m: m.set_value(theta.get_value() / DEGREES)
        )
        label.add_updater(lambda m: self.add_fixed_in_frame_mobjects(m))

        self.wait(5)


        

        
        # Build axis text as one MathTex expression
        axis_text = MathTex(
            r"\mathbf{u} = (",
            rf"\textcolor[HTML]{{FF3333}}{{{get_axis()[0]:.2f}}}", ",",
            rf"\textcolor[HTML]{{9B30FF}}{{{get_axis()[1]:.2f}}}", ",",
            rf"\textcolor[HTML]{{1E90FF}}{{{get_axis()[2]:.2f}}}", ")",
            font_size=50,
            tex_template=my_tex_template,
        ).move_to(LEFT * 4.4 + UP * 1)
        
        self.add_fixed_in_frame_mobjects(axis_text)




        # Animate end extending out to full Line
        self.play(
            Create(line),
            line.animate.put_start_and_end_on(-3*normalize(get_axis()), 3*normalize(get_axis())),
            line.animate.set_opacity(100),
            Write(axis_text),
            run_time=2
        )
         
        line.add_updater(lambda m: self.bring_to_back(m))
                     
        axis_text.add_updater(lambda m: m.become(MathTex(
            r"\mathbf{u} = (",
            rf"\textcolor[HTML]{{FF3333}}{{{get_axis()[0]:.2f}}}", ",",
            rf"\textcolor[HTML]{{9B30FF}}{{{get_axis()[1]:.2f}}}", ",",
            rf"\textcolor[HTML]{{1E90FF}}{{{get_axis()[2]:.2f}}}", ")",
            font_size=50,
            tex_template=my_tex_template,
        ).move_to(LEFT * 4.4 + UP * 1)))
        
        # Keep text fixed to screen
        axis_text.add_updater(lambda m: self.add_fixed_in_frame_mobjects(m))
        
        
        
        self.wait(2)

        with tempconfig({"disable_caching": True}):
            # Perform the rotation animation
            self.play(
                theta.animate.increment_value(720 * DEGREES), #   FIRST SPIN
                run_time=50,  # duration of the animation
                rate_func=rate_functions.ease_in_out_sine
            )
        
        self.wait(5)
        
        
        trails = [
            TracedPath(dot.get_center, stroke_color=dot.get_color(), stroke_width=2, dissipating_time=0)
            for dot in [dot1, dot2, dot3, dot4, dot5, dot6, dot7, dot8]
        ]
        for trail in trails:
            self.add(trail)
        
        
        with tempconfig({"disable_caching": True}):
            self.play(
                theta.animate.increment_value(-360 * DEGREES),#  SECOND SPIN WITH TRAIL
                run_time=40,
                rate_func=rate_functions.ease_in_out_sine
            )



        self.wait(10)
        
        

        self.play(Transform(text, MathTex(
            r"p_2 = q * (0, \pm 1, \pm 1, \pm 1)",
            font_size=50
        ).move_to(LEFT * 4 + UP * 3)))
        self.add_fixed_in_frame_mobjects(text)
        
        self.play(VGroup(*trails).animate.set_stroke(color=WHITE, width=2))


        
        _dot1 = Dot3D(color=dot_colors[0]).add_updater(lambda m: m.move_to(quaternion_multiply(q(dash=0), [0, 1, 1, 1])))
        _dot2 = Dot3D(color=dot_colors[1]).add_updater(lambda m: m.move_to(quaternion_multiply(q(dash=0), [0, 1, 1, -1])))
        _dot3 = Dot3D(color=dot_colors[2]).add_updater(lambda m: m.move_to(quaternion_multiply(q(dash=0), [0, 1, -1, 1])))
        _dot4 = Dot3D(color=dot_colors[3]).add_updater(lambda m: m.move_to(quaternion_multiply(q(dash=0), [0, 1, -1, -1])))
        _dot5 = Dot3D(color=dot_colors[4]).add_updater(lambda m: m.move_to(quaternion_multiply(q(dash=0), [0, -1, 1, 1])))
        _dot6 = Dot3D(color=dot_colors[5]).add_updater(lambda m: m.move_to(quaternion_multiply(q(dash=0), [0, -1, 1, -1])))
        _dot7 = Dot3D(color=dot_colors[6]).add_updater(lambda m: m.move_to(quaternion_multiply(q(dash=0), [0, -1, -1, 1])))
        _dot8 = Dot3D(color=dot_colors[7]).add_updater(lambda m: m.move_to(quaternion_multiply(q(dash=0), [0, -1, -1, -1])))
        
        _dots = [_dot1, _dot2, _dot3, _dot4, _dot5, _dot6, _dot7, _dot8]
    
        for d in _dots:
            d.update(0)
        
        _line1  = connect(_dot1, _dot2)
        _line2  = connect(_dot4, _dot3)
        _line3  = connect(_dot1, _dot3)
        _line4  = connect(_dot2, _dot4)
        _line5  = connect(_dot5, _dot6)
        _line6  = connect(_dot8, _dot7)
        _line7  = connect(_dot5, _dot7)
        _line8  = connect(_dot6, _dot8)
        _line9  = connect(_dot1, _dot5)
        _line10 = connect(_dot2, _dot6)
        _line11 = connect(_dot3, _dot7)
        _line12 = connect(_dot4, _dot8)
        
        _lines = [_line1, _line2, _line3, _line4, _line5, _line6, _line7, _line8, _line9, _line10, _line11, _line12]
        
        self.add(*_dots)
        self.add(*_lines)

    
        # Create and add polygon faces with optimized updaters
        _cube_faces = []
        for i, face_indices in enumerate(faces):
            color = face_colors[i]

            # Create face once
            face = Polygon(
                *[_dots[j].get_center() for j in face_indices],
                color=color,
                fill_color=color,
                stroke_opacity=0.8,
                fill_opacity=0.8,
                sheen_direction=UL,
                shade_in_3d=True
            )

            def face_updater(m, face_indices=face_indices):
                new_points = [_dots[j].get_center() for j in face_indices]
                # Update existing polygon instead of recreating
                m.set_points_as_corners(new_points + [new_points[0]])

            face.add_updater(face_updater)
            _cube_faces.append(face)
            self.add(face)

            
        
        VGroup(*_lines, *_dots, *_cube_faces).set_opacity(0)

  
            
        self.play(VGroup(*lines, *dots, *cube_faces).animate.set_opacity(0),
                  VGroup(*_lines, *_dots, *_cube_faces).animate.set_opacity(100),
                  )

            
        with tempconfig({"disable_caching": True}):    
            self.play(
                theta.animate.increment_value(-720 * DEGREES),  # THIRD SPIN JUST _CUBE
                run_time=50,  # duration of the animation
                rate_func=rate_functions.ease_in_out_sine
            )
        
        

        self.wait(2)
       
        text2 = MathTex(
            r"p_1 = (0, \pm 1, \pm 1, \pm 1) * q",
            font_size=50
        ).move_to(RIGHT * 4 + UP * 3)
        self.add_fixed_in_frame_mobjects(text2)
        
    
            
        self.play(Write(text2), Unwrite(VGroup(*trails)))
        
        self.play(VGroup(*lines, *dots, *cube_faces).animate.set_opacity(100))
        
        self.wait(2)
        
        with tempconfig({"disable_caching": True}):      
            self.play(
                theta.animate.increment_value(360 * DEGREES),  # FOURTH SPIN BOTH CUBES
                run_time=50,  # duration of the animation
                rate_func=rate_functions.ease_in_out_sine
            )
            
        for mob in trails:
            mob.clear_updaters()
        
        self.wait(10)
        
        self.play(Unwrite(text2))
        
        self.play(Transform(text, MathTex(
            r"p_2 = q * (0, \pm 1, \pm 1, \pm 1) * q",
            font_size=45
        ).move_to(LEFT * 4.1 + UP * 3)))
        self.add_fixed_in_frame_mobjects(text)
        
        
        self.play(VGroup(*lines, *dots, *cube_faces).animate.set_opacity(0))
        
        
        for mob in _dots:
            mob.clear_updaters()
            
          
        _dot1.add_updater(lambda m: m.move_to(quaternion_multiply(q(dash=0), quaternion_multiply([0, 1, 1, 1], q(dash=0), w=True))))
        _dot2.add_updater(lambda m: m.move_to(quaternion_multiply(q(dash=0), quaternion_multiply([0, 1, 1, -1], q(dash=0), w=True))))
        _dot3.add_updater(lambda m: m.move_to(quaternion_multiply(q(dash=0), quaternion_multiply([0, 1, -1, 1], q(dash=0), w=True))))
        _dot4.add_updater(lambda m: m.move_to(quaternion_multiply(q(dash=0), quaternion_multiply([0, 1, -1, -1], q(dash=0), w=True))))
        _dot5.add_updater(lambda m: m.move_to(quaternion_multiply(q(dash=0), quaternion_multiply([0, -1, 1, 1], q(dash=0), w=True))))
        _dot6.add_updater(lambda m: m.move_to(quaternion_multiply(q(dash=0), quaternion_multiply([0, -1, 1, -1], q(dash=0), w=True))))
        _dot7.add_updater(lambda m: m.move_to(quaternion_multiply(q(dash=0), quaternion_multiply([0, -1, -1, 1], q(dash=0), w=True))))
        _dot8.add_updater(lambda m: m.move_to(quaternion_multiply(q(dash=0), quaternion_multiply([0, -1, -1, -1], q(dash=0), w=True))))
        
        with tempconfig({"disable_caching": True}):
            self.play(
                theta.animate.increment_value(720 * DEGREES),  # FIFTH SPIN DOUBLE MULTIPLY
                run_time=50,  # duration of the animation
                rate_func=rate_functions.ease_in_out_sine
            )
        
        
        self.wait(15)
        
        for mob in _dots:
            mob.clear_updaters()
            
          
        _dot1.add_updater(lambda m: m.move_to(quaternion_multiply(q(dash=0), quaternion_multiply([0, 1, 1, 1], q(dash=1), w=True))))
        _dot2.add_updater(lambda m: m.move_to(quaternion_multiply(q(dash=0), quaternion_multiply([0, 1, 1, -1], q(dash=1), w=True))))
        _dot3.add_updater(lambda m: m.move_to(quaternion_multiply(q(dash=0), quaternion_multiply([0, 1, -1, 1], q(dash=1), w=True))))
        _dot4.add_updater(lambda m: m.move_to(quaternion_multiply(q(dash=0), quaternion_multiply([0, 1, -1, -1], q(dash=1), w=True))))
        _dot5.add_updater(lambda m: m.move_to(quaternion_multiply(q(dash=0), quaternion_multiply([0, -1, 1, 1], q(dash=1), w=True))))
        _dot6.add_updater(lambda m: m.move_to(quaternion_multiply(q(dash=0), quaternion_multiply([0, -1, 1, -1], q(dash=1), w=True))))
        _dot7.add_updater(lambda m: m.move_to(quaternion_multiply(q(dash=0), quaternion_multiply([0, -1, -1, 1], q(dash=1), w=True))))
        _dot8.add_updater(lambda m: m.move_to(quaternion_multiply(q(dash=0), quaternion_multiply([0, -1, -1, -1], q(dash=1), w=True))))
        
        
        self.play(Transform(text, MathTex(
            r"p_3 = q * (0, \pm 1, \pm 1, \pm 1) * q'",
            font_size=45
        ).move_to(LEFT * 4.1 + UP * 3)))
        self.add_fixed_in_frame_mobjects(text)
        
        with tempconfig({"disable_caching": True}):
            self.play(
                theta.animate.increment_value(-600 * DEGREES),  # SIXTH SPIN REAL ROTATION
                run_time=50,  # duration of the animation
                rate_func=rate_functions.ease_in_out_sine
            )
        
        self.wait(10)

        with tempconfig({"disable_caching": True}):
            self.play(
                axis_dot.animate.move_to([0, -1, 0.6]),
                run_time=5,
                func_rate=linear,
            )
            self.play(
                axis_dot.animate.move_to([2, 0.3, -4]),
                run_time=5,
                func_rate=linear,
            )
            self.play(
                axis_dot.animate.move_to([0, 1, 0]),
                run_time=5,
                func_rate=linear,
            )
            self.play(
                theta.animate.increment_value(-120 * DEGREES),  # SIXTH SPIN REAL ROTATION
                run_time=5,  # duration of the animation
                rate_func=rate_functions.ease_in_out_sine
            )
        
        
        self.wait(8)
            
        for mob in self.mobjects:
            mob.clear_updaters()
        
        self.wait(8)
    

        self.play(*[FadeOut(mob) for mob in self.mobjects])
                
        self.wait()      



class QuaternionMultiplication(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()

        # zoom out so we see the axes
        self.set_camera_orientation(zoom=0.5)

        self.play(FadeIn(axes))

        # start position
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=1.5, func_rate=rate_functions.ease_in_out_sine)
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.wait(0.5)

        # --- Quaternion basis vectors i, j, k ---
        i_vec = Arrow3D(start=ORIGIN, end=[2, 0, 0], color=RED)     # i along x-axis
        j_vec = Arrow3D(start=ORIGIN, end=[0, 2, 0], color=GREEN)   # j along y-axis
        k_vec = Arrow3D(start=ORIGIN, end=[0, 0, 2], color=BLUE)    # k along z-axis

        # Animate arrows growing
        self.play(Create(i_vec))
        self.play(Create(j_vec))
        self.play(Create(k_vec))
        
        i_label = MathTex("i", color=RED).move_to([2.3, 0, 0])
        j_label = MathTex("j", color=GREEN).move_to([0, 2.3, 0])
        k_label = MathTex("k", color=BLUE).move_to([0, 0, 2.3])

        # Make labels always face camera
        self.add_fixed_orientation_mobjects(i_label, j_label, k_label)
        
        self.play(Write(VGroup(i_label, j_label, k_label)), FadeOut(axes))
        self.move_camera(zoom=1.5)

        self.wait()
        
        
        
        eq1 = MathTex("i j = k",
                      font_size=100,
                      tex_to_color_map={"i": RED, "j": GREEN, "k": BLUE, "=": WHITE, "(": WHITE, ")": WHITE, "-": WHITE}
        ).to_edge(DOWN, buff=1)
        eq2 = MathTex("j k = i",
                      font_size=100,
                      tex_to_color_map={"i": RED, "j": GREEN, "k": BLUE, "=": WHITE, "(": WHITE, ")": WHITE, "-": WHITE}
        ).to_edge(DOWN, buff=1)
        eq3 = MathTex("k i = j",
                      font_size=100,
                      tex_to_color_map={"i": RED, "j": GREEN, "k": BLUE, "=": WHITE, "(": WHITE, ")": WHITE, "-": WHITE}
        ).to_edge(DOWN, buff=1)
        eq4 = MathTex("k j = (-i)",
                      font_size=100,
                      tex_to_color_map={"i": RED, "j": GREEN, "k": BLUE, "=": WHITE, "(": WHITE, ")": WHITE, "-": WHITE}
        ).to_edge(DOWN, buff=1)
        eq5 = MathTex("j (-i) = k",
                      font_size=100,
                      tex_to_color_map={"i": RED, "j": GREEN, "k": BLUE, "=": WHITE, "(": WHITE, ")": WHITE, "-": WHITE}
        ).to_edge(DOWN, buff=1)
        eq6 = MathTex("(-i) k = j",
                      font_size=100,
                      tex_to_color_map={"i": RED, "j": GREEN, "k": BLUE, "=": WHITE, "(": WHITE, ")": WHITE, "-": WHITE}
        ).to_edge(DOWN, buff=1)
        
        
        self.add_fixed_in_frame_mobjects(eq1)
        self.play(Write(eq1))
        
        self.wait(2)
        
        
        # create 2 arrows
        
        i_tip = [2, 0.2, 0]
        j_tip = [0.2, 2, 0]


        arc1 = ArcBetweenPoints(i_tip, j_tip, angle=PI/2, color=YELLOW)
        arrow1 = Arrow3D(arc1.point_from_proportion(0.8), arc1.point_from_proportion(1.0), color=YELLOW, stroke_width=0)
        self.play(Create(arc1), Create(arrow1))
        self.wait()
        
        j_tip = [0, 2, 0.2]
        k_tip = [0, 0.2, 2]

   
        arc2 = ArcBetweenPoints(j_tip, k_tip, angle=PI/2, color=YELLOW)
        arrow2 = Arrow3D(arc2.point_from_proportion(0.8), arc2.point_from_proportion(1.0), color=YELLOW, stroke_width=0)
        self.play(Create(arc2), Create(arrow2))
        self.wait()
        
        
        
        # rotate the arrows around
        
        arrows = VGroup(arc1, arrow1, arc2, arrow2)
        axis = normalize(np.array([1, 1, 1]))
        axis2 = normalize(np.array([0, 1, 0]))
        axis3 = normalize(np.array([-1, 1, 1]))

        

        self.play(Rotate(arrows, angle=2*PI/3, axis=axis, about_point=ORIGIN, run_time=2), TransformMatchingTex(eq1, eq2))    
        self.add_fixed_in_frame_mobjects(eq2)
        self.wait(2)
        
        self.play(Rotate(arrows, angle=2*PI/3, axis=axis, about_point=ORIGIN, run_time=2), TransformMatchingTex(eq2, eq3))    
        self.add_fixed_in_frame_mobjects(eq3)
        self.wait(2)
        
        self.play(Rotate(arrows, angle=2*PI/3, axis=axis, about_point=ORIGIN, run_time=2), TransformMatchingTex(eq3, eq1))    
        self.add_fixed_in_frame_mobjects(eq1)
        self.wait(2)
        
        
        self.move_camera(phi=75 * DEGREES, theta=150 * DEGREES, zoom=1.5, run_time=1.5, func_rate=rate_functions.ease_in_out_sine)
        self.set_camera_orientation(phi=75 * DEGREES, theta=150 * DEGREES)
        self.wait(0.5)
          
        neg_i_vec = Arrow3D(start=ORIGIN, end=[-2,0,0], color=RED)
        neg_i_label = MathTex("-i", color=RED).move_to([-2.3, 0, 0])
        self.add_fixed_orientation_mobjects(neg_i_label)

        self.play(Transform(i_vec, neg_i_vec), FadeOut(i_label), Write(neg_i_label), run_time=2)
        self.wait()
        
        self.add_fixed_in_frame_mobjects(eq4)
        self.play(Rotate(arrows, angle=-PI/2, axis=axis2, about_point=ORIGIN, run_time=2), FadeOut(eq1), FadeIn(eq4))
        self.wait(2)
        

        self.play(Rotate(arrows, angle=2*PI/3, axis=axis3, about_point=ORIGIN, run_time=2), TransformMatchingTex(eq4, eq5))
        self.add_fixed_in_frame_mobjects(eq5)
        self.wait(2)

        self.play(Rotate(arrows, angle=2*PI/3, axis=axis3, about_point=ORIGIN, run_time=2), TransformMatchingTex(eq5, eq6))
        self.add_fixed_in_frame_mobjects(eq6)
        self.wait(2)

        self.play(Rotate(arrows, angle=2*PI/3, axis=axis3, about_point=ORIGIN, run_time=2), TransformMatchingTex(eq6, eq4))
        self.add_fixed_in_frame_mobjects(eq4)
        self.wait(5)

                
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        


class QuaternionMultiplicationProgressive(Scene):
    def construct(self):

        # Color map
        color_map = {"i": RED, "j": GREEN, "k": BLUE}

        # Start with i^2 = -1
        eq_text = MathTex("i^2 = -1", font_size=100, substrings_to_isolate=["i"])
        eq_text.set_color_by_tex("i", RED)
        eq_text.to_edge(UP, buff=1.5)
        self.play(FadeIn(eq_text))
        self.wait(2)

        # Step 2: add j^2 = -1
        eq_text_next = MathTex("i^2 = j^2 = -1", font_size=100, substrings_to_isolate=["i","j"])
        eq_text_next.set_color_by_tex("i", RED)
        eq_text_next.set_color_by_tex("j", GREEN)
        eq_text_next.to_edge(UP, buff=1.5)
        self.play(TransformMatchingTex(eq_text, eq_text_next))
        eq_text = eq_text_next  # update reference
        self.wait()

        # Step 3: add k^2 = -1
        eq_text_next = MathTex("i^2 = j^2 = k^2 = -1", font_size=100, substrings_to_isolate=["i","j","k"])
        eq_text_next.set_color_by_tex("i", RED)
        eq_text_next.set_color_by_tex("j", GREEN)
        eq_text_next.set_color_by_tex("k", BLUE)
        eq_text_next.to_edge(UP, buff=1.5)
        self.play(TransformMatchingTex(eq_text, eq_text_next))
        eq_text = eq_text_next
        self.wait()

        # Step 4: add ijk = -1
        eq_text_next = MathTex("i^2 = j^2 = k^2 = ijk = -1", font_size=100, substrings_to_isolate=["i","j","k","ijk"])
        eq_text_next.set_color_by_tex("i", RED)
        eq_text_next.set_color_by_tex("j", GREEN)
        eq_text_next.set_color_by_tex("k", BLUE)
        eq_text_next.set_color_by_tex("ijk", BLUE)
        eq_text_next.to_edge(UP, buff=1.5)
        self.play(TransformMatchingTex(eq_text, eq_text_next))
        eq_text = eq_text_next
        self.wait()


        # --- Pairwise multiplications ---
        rules = [
            (("i", "j", "k"), ("j", "i", "-k")),
            (("j", "k", "i"), ("k", "j", "-i")),
            (("k", "i", "j"), ("i", "k", "-j")),
        ]

        start_y = 0.5  # below the special rule

        for idx, (pair1, pair2) in enumerate(rules):
            group_texs = []

            for a, b, result in [pair1, pair2]:
                # Left and right terms
                a_tex = MathTex(a, font_size=100, color=color_map.get(a.strip("-"), WHITE))
                b_tex = MathTex(b, font_size=100, color=color_map.get(b.strip("-"), WHITE))
                mult_tex = MathTex(r"\cdot", font_size=100)
                arrow = MathTex(r"\rightarrow", font_size=100)
                res_tex = MathTex(result, font_size=100, color=color_map.get(result.strip("-"), WHITE))

                # Arrange horizontally for this pair
                expr = VGroup(a_tex, mult_tex, b_tex, arrow, res_tex).arrange(RIGHT, buff=0.5)
                group_texs.append(expr)

            # Arrange both pairs on the same line
            line = VGroup(*group_texs).arrange(RIGHT, buff=2)  # space between noncommutative pairs
            line.move_to([0, start_y - idx*1.2, 0])

            # Animate all elements of the line
            for expr in group_texs:
                for n in range(len(expr)):
                    self.play(FadeIn(expr[n]), run_time=0.3)
                    if n == 3:
                        self.wait(0.3)
                self.wait(0.3)

        self.wait(2)


        # Recursive function to collect all MathTex submobjects
        def collect_mathtex(mobj):
            math_list = []
            if isinstance(mobj, MathTex):
                math_list.append(mobj)
            if hasattr(mobj, "submobjects"):
                for sub in mobj.submobjects:
                    math_list.extend(collect_mathtex(sub))
            return math_list

        # Collect all MathTex objects in the scene
        all_mathtex = []
        for mobj in self.mobjects:
            all_mathtex.extend(collect_mathtex(mobj))

        # Transform dots to asterisks and arrows to equals
        transforms = []
        for subtex in all_mathtex:
            text = subtex.get_tex_string()
            new_text = text.replace(r"\cdot", "*").replace(r"\rightarrow", "=")
            if new_text != text:
                new_tex = MathTex(new_text, font_size=subtex.font_size)
                new_tex.set_color(subtex.get_color())
                new_tex.move_to(subtex)
                transforms.append(Transform(subtex, new_tex))

        if transforms:
            self.play(*transforms, run_time=0.5)
            
            
        self.wait(5)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        


class QuaternionMultiplicationFull(Scene):
    def construct(self):
        
        def new_pos(q1_index, q2_index):
            col_spacing = 2.5
            row_spacing = 0.8
            x_offset = (q2_index - (4 - 1) / 2) * col_spacing
            y_offset = q1_index * row_spacing
            return x_offset * RIGHT + y_offset * DOWN

        
        def update_pair(pair_group, this_step, q1_index, q2_index):
            if this_step[q1_index][q2_index] == self.old_step[q1_index][q2_index]:
                return None
            target = MathTex(*this_step[q1_index][q2_index].split(' '))
            target.set_color_by_tex("i", RED)
            target.set_color_by_tex("j", GREEN)
            target.set_color_by_tex("k", BLUE)
            target.move_to(new_pos(q1_index, q2_index))
            return TransformMatchingTex(pair_group, target), target
        

        def transform_step(this_step, wait):
            for n, pair_group in enumerate(self.pair_groups):        
                animation = update_pair(pair_group, this_step, n // 4, n % 4)
                if animation is not None:
                    animation, new_target = animation
                    self.play(animation)
                    self.pair_groups[n] = new_target
                if wait > 0:
                    self.wait(wait)
            self.old_step = this_step
            
            
        
        q1_parts = [r"a_1", r"b_1 i", r"c_1 j", r"d_1 k"]
        q2_parts = [r"a_2", r"b_2 i", r"c_2 j", r"d_2 k"]

        q1_tex = MathTex(r"q_1 = ", *(r" + ".join(q1_parts).split(' ')), font_size=50)
        q2_tex = MathTex(r"q_2 = ", *(r" + ".join(q2_parts).split(' ')), font_size=50)
        q1_tex.set_color_by_tex("i", RED).set_color_by_tex("j", GREEN).set_color_by_tex("k", BLUE)
        q2_tex.set_color_by_tex("i", RED).set_color_by_tex("j", GREEN).set_color_by_tex("k", BLUE)

        q1_tex.to_edge(UP)
        q2_tex.next_to(q1_tex, DOWN, buff=0.5)
        self.play(FadeIn(q1_tex), FadeIn(q2_tex))
        self.wait(1)

        mult_tex = MathTex(r"q_1 * q_2 = ", font_size=50).next_to(q2_tex, DOWN, buff=1)
        self.play(Write(mult_tex))

        # Step 4: Create a grid of source positions
        coef_idxs = [1, 3, 6, 9]
        unit_idxs = [None, 4, 7, 10]
            
        
        self.old_step = [['', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']]
        
        this_step = [[r"+ a_1 a_2", r"+ a_1 b_2 i", r"+ a_1 c_2 j", r"+ a_1 d_2 k"],
                     [r"+ b_1 i a_2", r"+ b_1 i b_2 i", r"+ b_1 i c_2 j", r"+ b_1 i d_2 k"],
                     [r"+ c_1 j a_2", r"+ c_1 j b_2 i", r"+ c_1 j c_2 j", r"+ c_1 j d_2 k"],
                     [r"+ d_1 k a_2", r"+ d_1 k b_2 i", r"+ d_1 k c_2 j", r"+ d_1 k d_2 k"],
                     ]
        

        self.pair_groups = []
        for q1_index in range(4):
            u1 = VGroup(q1_tex[coef_idxs[q1_index]], (q1_tex[unit_idxs[q1_index]] if q1_index > 0 else MathTex("")))
            for q2_index in range(4):
                u2 = VGroup(q2_tex[coef_idxs[q2_index]], (q2_tex[unit_idxs[q2_index]] if q2_index > 0 else MathTex("")))
                
                u1_copy, u2_copy = u1.copy(), u2.copy()
                
                self.play(Indicate(u1, scale_factor=1.2, color=YELLOW),
                          Indicate(u2, scale_factor=1.2, color=YELLOW),
                          run_time=0.3,
                          )
                
                pair_group = VGroup(u1_copy, u2_copy)
                self.add(pair_group)

                target = MathTex(*this_step[q1_index][q2_index].split(' '))
                target.set_color_by_tex("i", RED)
                target.set_color_by_tex("j", GREEN)
                target.set_color_by_tex("k", BLUE)
                target.move_to(new_pos(q1_index, q2_index))
                

                self.play(TransformMatchingShapes(pair_group, target))
                self.pair_groups.append(target)
              
                
                
                

        self.wait(1)
        
        self.play(*[Indicate(mob) for mob in self.pair_groups])
        
        
        transform_step([[r"+ a_1 a_2", r"+ a_1 b_2 i", r"+ a_1 c_2 j", r"+ a_1 d_2 k"],
                     [r"+ b_1 a_2 i", r"+ b_1 b_2 i i", r"+ b_1 c_2 i j", r"+ b_1 d_2 i k"],
                     [r"+ c_1 a_2 j", r"+ c_1 b_2 j i", r"+ c_1 c_2 j j", r"+ c_1 d_2 j k"],
                     [r"+ d_1 a_2 k", r"+ d_1 b_2 k i", r"+ d_1 c_2 k j", r"+ d_1 d_2 k k"],
                     ],
                       wait=0,
                       )

        self.wait(1)


        transform_step([[r"+ a_1 a_2", r"+ a_1 b_2 i", r"+ a_1 c_2 j", r"+ a_1 d_2 k"],
                     [r"+ b_1 a_2 i", r"+ b_1 b_2 (-1)", r"+ b_1 c_2 k", r"+ b_1 d_2 (-j)"],
                     [r"+ c_1 a_2 j", r"+ c_1 b_2 (-k)", r"+ c_1 c_2 (-1)", r"+ c_1 d_2 i"],
                     [r"+ d_1 a_2 k", r"+ d_1 b_2 j", r"+ d_1 c_2 (-i)", r"+ d_1 d_2 (-1)"],
                     ],
                       wait=1,
                       )
            
        
        self.wait(2)
            
        transform_step([[r"+ a_1 a_2", r"+ a_1 b_2 i", r"+ a_1 c_2 j", r"+ a_1 d_2 k"],
                     [r"+ b_1 a_2 i", r"- b_1 b_2", r"+ b_1 c_2 k", r"- b_1 d_2 j"],
                     [r"+ c_1 a_2 j", r"- c_1 b_2 k", r"- c_1 c_2", r"+ c_1 d_2 i"],
                     [r"+ d_1 a_2 k", r"+ d_1 b_2 j", r"- d_1 c_2 i", r"- d_1 d_2"],
                     ],
                       wait=0.5,
                       )
        
        
        
        
        target_rows = [[0, 1, 2, 3],
                        [1, 0, 3, 2],
                        [2, 3, 0, 1],
                        [3, 2, 1, 0],
                      ]

        for col in range(4):          
            col_terms = [self.pair_groups[row * 4 + col] for row in range(4)]
            
            self.play(*[
                term.animate.move_to(new_pos(target_rows[col][n], col))
                for n, term in enumerate(col_terms)
            ])
            self.wait(0.5)
            
            
            
        
        
        strings = [
                    r"a_1 a_2 - b_1 b_2 - c_1 c_2 - d_1 d_2",
                    r"+ b_1 a_2 i + a_1 b_2 i - d_1 c_2 i + c_1 d_2 i",
                    r"+ c_1 a_2 j + d_1 b_2 j + a_1 c_2 j - b_1 d_2 j",
                    r"+ d_1 a_2 k - c_1 b_2 k + b_1 c_2 k + a_1 d_2 k",
                 ]

        rows = []
        for row in range(4):
            col_terms = [self.pair_groups[target_rows[col].index(row) * 4 + col] for col in range(4)]
            
            target = MathTex(*strings[row].split(' '), font_size=50)
            target.set_color_by_tex("i", RED)
            target.set_color_by_tex("j", GREEN)
            target.set_color_by_tex("k", BLUE)
            target.move_to(new_pos(row, 1.5))
            
            self.play(TransformMatchingTex(VGroup(*col_terms), target))
            self.wait(0.5)
            rows.append(target)
            
            
            
        strings = [
                    r"a_1 a_2 - b_1 b_2 - c_1 c_2 - d_1 d_2",
                    r"+ ( b_1 a_2 + a_1 b_2 - d_1 c_2 + c_1 d_2 ) i",
                    r"+ ( c_1 a_2 + d_1 b_2 + a_1 c_2 - b_1 d_2 ) j",
                    r"+ ( d_1 a_2 - c_1 b_2 + b_1 c_2 + a_1 d_2 ) k",
                 ]

        for row in range(4):
            
            target = MathTex(*strings[row].split(' '), font_size=50)
            target.set_color_by_tex("i", RED)
            target.set_color_by_tex("j", GREEN)
            target.set_color_by_tex("k", BLUE)
            target.move_to(new_pos(row, 1.5))
            
            self.play(TransformMatchingTex(rows[row], target))
            self.wait(0.5)
            rows[row] = target
            
            
            
        final_string = r"""
        & a_1 a_2 - b_1 b_2 - c_1 c_2 - d_1 d_2 \\
        + ( & b_1 a_2 + a_1 b_2 - d_1 c_2 + c_1 d_2 ) i \\
        + ( & c_1 a_2 + d_1 b_2 + a_1 c_2 - b_1 d_2 ) j \\
        + ( & d_1 a_2 - c_1 b_2 + b_1 c_2 + a_1 d_2 ) k
        """

        final_tex = MathTex(*final_string.split(), font_size=50)
        final_tex.set_color_by_tex("i", RED)
        final_tex.set_color_by_tex("j", GREEN)
        final_tex.set_color_by_tex("k", BLUE)
        final_tex.move_to(new_pos(1.5, 1.5))

        self.play(TransformMatchingTex(VGroup(*rows), final_tex))
        self.wait(2)


class FinalFormulas(Scene):
    def construct(self):
        # Create the formulas using MathTex for LaTeX rendering
        title = Text("Quaternion Rotation Formulas").to_edge(UP)

        main_formula = MathTex(
            "p'", "=", "qpq^{-1}"
        )

        q_formula = MathTex(
            "q", "=", r"(\cos(\frac{\theta}{2}), u_x\sin(\frac{\theta}{2}), u_y\sin(\frac{\theta}{2}), u_z\sin(\frac{\theta}{2}))"
        ).next_to(main_formula, DOWN, buff=0.75)

        p_formula = MathTex(
            "p", "=", "(0, p_x, p_y, p_z)"
        ).next_to(q_formula, DOWN, buff=0.75)

        q_inv_formula = MathTex(
            "q^{-1}", "=", "q^*", "=", r"(\cos(\frac{\theta}{2}), -u_x\sin(\frac{\theta}{2}), -u_y\sin(\frac{\theta}{2}), -u_z\sin(\frac{\theta}{2}))"
        ).next_to(p_formula, DOWN, buff=0.75)

        # Arrange the formulas in a VGroup and center them
        all_formulas = VGroup(
            main_formula, q_formula, p_formula, q_inv_formula
        ).center()

        # Add the title and the formula group to the scene
        self.add(title, all_formulas)
        self.wait(5)
           
            
            
            