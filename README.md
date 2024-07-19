# Career Tree
![Career Tree](https://github.com/O-79/CareerTree-py/blob/master/resources/icon_base_black_v1.1.png?raw=true)<em> Document Author: Adi</em>

todo: export in markdown, include job salaries somewhere

<h3>Run in GUI</h3>
<code>python CareerTree.py</code>

<h3>Run in CLI</h3>
<code>python Control.py</code>

<h3>What Is It?</h3>

Career Tree is a tool primarily made for high school students / graduates which creates *a tree to map potential career paths* starting from the single root, the desired location.

Generative AI (ChatGPT) will be used to list potential:
| Content | Branch Level |
| --- | --- |
| Careers *in fixed location* | Level 1 |
| Jobs *based on career, in fixed location* | Level 2 |
| School *based on desired job (& degree), in fixed or variable location* | Level 3 |
> Degree information: Dependent on selected job\
> School information: Costs, loan average & programs, grant opportunities, *time to repay cost of education; dependent on selected job & internal calculations*

ChatGPT's responses will be based on a selected *response size, X*, which is a constant used at all branch levels of the tree to generate an *X* number of careers based on location, jobs based on career, etc.
> For example, X = 6 gives the following maximum tree size (nodes per level): 1 -> 6 -> 36 -> 216

<h3>An Example Career Tree (Put In Text)</h3>
<details>
  ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄<br/>
  Powered by: gpt-3.5-turbo<br/>
  Response Size: <b>4</b><br/>
  ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄<br/>
  <b>LOCATION:</b> North Carolina<br/>
  &emsp;&emsp;&emsp;╍┫ <b>CAREER:</b> Medical<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍┫ <b>JOB:</b> Nurse<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍┫ <b>JOB:</b> General Practitioner<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍┫ <b>JOB:</b> Dentist<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍┫ <b>JOB:</b> Veterinarian<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍═ <em>Salary:</em>  $$$<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍┫ <b>COLLEGE:</b> Duke University<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍═ <em>Requirements:</em>   XYZ<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍═ <em>Tuition:</em>        $$$<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍═ <em>Avg. Loan:</em>      $$$<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍═ <em>Loan Programs:</em>  A, B, C, X, Y, Z<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍═ <em>Time to Repay:</em>  X.Y months<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍┫ <b>COLLEGE:</b> University of North Carolina at Chapel Hill<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍┫ <b>COLLEGE:</b> Wake Forest University<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍┫ <b>COLLEGE:</b> East Carolina University<br/>
  &emsp;&emsp;&emsp;╍┫ <b>CAREER:</b> Data Scientist<br/>
  &emsp;&emsp;&emsp;╍┫ <b>CAREER:</b> Software Engineering<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍┫ <b>JOB:</b> Frontend Developer<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍┫ <b>JOB:</b> Backend Developer<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍┫ <b>JOB:</b> Cybersecurity Specialist<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍═ <em>Salary:</em>  $$$<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍┫ <b>COLLEGE:</b> North Carolina State University<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍═ <em>Requirements:</em>   XYZ<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍═ <em>Tuition:</em>        $$$<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍═ <em>Avg. Loan:</em>      $$$<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍═ <em>Loan Programs:</em>  A, B, C, X, Y, Z<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍═ <em>Time to Repay:</em>  X.Y months<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍┫ <b>COLLEGE:</b> University of North Carolina at Chapel Hill<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍┫ <b>COLLEGE:</b> University of North Carolina at Charlotte<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍═ <em>Requirements:</em>   XYZ<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍═ <em>Tuition:</em>        $$$<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍═ <em>Avg. Loan:</em>      $$$<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍═ <em>Loan Programs:</em>  A, B, C, X, Y, Z<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍═ <em>Time to Repay:</em>  X.Y months<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍┫ <b>COLLEGE:</b> Duke University<br/>
  &emsp;&emsp;&emsp;╍&emsp;&emsp;&emsp;╍┫ <b>JOB:</b> Videogame Developer<br/>
  &emsp;&emsp;&emsp;╍┫ <b>CAREER:</b> Marketing<br/>
  ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄<br/>
</details>

![Career Tree](https://github.com/O-79/CareerTree-py/blob/master/resources/icon_full_borderless_shadow_v1.1.png?raw=true)
