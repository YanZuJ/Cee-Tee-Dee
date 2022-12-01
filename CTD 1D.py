#!/usr/bin/env python
# coding: utf-8

# In[1]:


##happy face
import turtle
t=turtle.Turtle()
t.hideturtle()
t.color('green')
t.speed(6)
radius=100
extent=360

t.color('yellow')
t.begin_fill()
t.circle(radius,extent)##main circle
t.end_fill()

t.penup()
t.setposition(-50,100)
t.pendown()
radius=25
extent=360




t.color('white')
t.begin_fill()
t.circle(radius,extent)##first eye
t.end_fill()

t.penup()
t.setposition(50,100)
t.pendown()
radius=25
extent=360

t.begin_fill()
t.circle(radius,extent)
t.end_fill()##second eye
t.penup()

t.color('black')
t.begin_fill()
t.penup()
t.setposition(-50,110)
t.pendown()
radius=12.5
extent=360
t.circle(radius,extent)
t.end_fill()
t.penup()

t.color('black')
t.begin_fill()
t.penup()
t.setposition(50,110)
t.pendown()
radius=12.5
extent=360
t.circle(radius,extent)
t.end_fill()
t.penup()

t.color('red')
t.begin_fill()
t.setposition(0,20)
t.pendown()
t.circle(50,90)
t.left(90)
t.forward(100)
t.left(90)
t.circle(50,90)
t.end_fill()





# In[1]:


##sad face 
import turtle
t=turtle.Turtle()
t.hideturtle()
t.color('green')
t.speed(6)
radius=100
extent=360

t.color('yellow')
t.begin_fill()
t.circle(radius,extent)##main circle
t.end_fill()

t.penup()
t.setposition(-50,100)
t.pendown()
radius=25
extent=360

t.color('white')
t.begin_fill()
t.circle(radius,extent)##first eye
t.end_fill()

t.penup()
t.setposition(50,100)
t.pendown()
radius=25
extent=360

t.begin_fill()
t.circle(radius,extent)
t.end_fill()##second eye
t.penup()

t.color('black')
t.begin_fill()
t.penup()
t.setposition(-50,110)
t.pendown()
radius=12.5
extent=360
t.circle(radius,extent)
t.end_fill()
t.penup()

t.color('black')
t.begin_fill()
t.penup()
t.setposition(50,110)
t.pendown()
radius=12.5
extent=360
t.circle(radius,extent)
t.end_fill()
t.penup()



t.circle(radius,extent)
t.penup()
t.setposition(0,100)
t.pendown()
t.color('red')
t.begin_fill()
t.circle(-50,90)
t.right(90)
t.forward(100)
t.right(90)
t.circle(-50,90)
t.end_fill()


# In[ ]:





# In[ ]:




