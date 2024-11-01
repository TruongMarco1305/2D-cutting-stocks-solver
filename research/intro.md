Author: Tran Bao Phuc Long - 2352703
## **Intro**
The Cutting Stock Problem (CSP) is a classic optimization challenge that arises in various industries. Introduced by P.C.Gilmore and R.E.Gomory in the 1960s, CSP has evolved significantly, impacting businesses such as manufacturing, textiles, and packaging, where material efficiency directly influences costs. The core objective of CSP is to determine how to cut larger stock materials into smaller pieces to meet demand while minimizing waste and maximizing the use of available resources. Due to its combinatorial nature and the exponential growth of potential solutions, the CSP is considered an NP-hard problem, requiring specialized algorithms and methods for practical solutions. 
##### Historical background and evolution
The initial work on the CSP focused on one-dimensional variants, where materials like paper rolls were cut into narrower strips. Gilmore and Gomory developed mathematical programming models and solution methodologies that laid the groundwork for modern research. Their approach utilized linear programming with column generation, which proved to be a significant step toward solving large-scale instances of the problem efficiently.

Over time, research expanded to two-dimensional and multi-dimensional variants, which are more applicable to industries dealing with sheets of material rather than simple linear rolls. The Two-Dimensional Cutting Stock Problem (2D CSP) emerged as an important field of study, with methods being adapted to handle complexities related to layout, orientation, and multiple constraints.

##### Significance in Various Industries
The CSP holds great importance in industries that prioritize material efficiency and cost reduction. For instance:

- **Manufacturing**: Metalworking, glass cutting, and wood processing plants need to optimize their cutting patterns to minimize scrap and meet production quotas.
- **Textiles**: The fashion and upholstery sectors face challenges in cutting fabrics into specific shapes with minimal waste.
- **Printing and Packaging**: Paper manufacturers and packaging companies use CSP solutions to optimize the cutting of large sheets into smaller pieces for printed materials or packaging designs.
- **Logistics and Construction**: Industries that deal with materials like plastic or insulation sheets also benefit from optimized cutting stock solutions.

An effective CSP solutions improve operational efficiency, lower material costs, and support sustainability initiatives by reducing waste.
##### Mathematical Models Used in CSP
Over the years, various mathematical models have been developed to represent and solve the CSP. These models differ based on the nature of the problem (e.g., one-dimensional or multi-dimensional) and the complexity of constraints involved. Some of the common models include:

- **Linear Programming (LP) and Integer Linear Programming (ILP)**: Core methods for exact solutions, employing column generation to optimize cutting patterns by solving sub-problems iteratively.
- **Knapsack-Based Models**: Represent CSP as an extension of the knapsack problem, focusing on maximizing the use of stock material within capacity limits.
- **Mixed-Integer Programming (MIP)**: Used for problems with additional constraints, such as minimizing the number of distinct cutting patterns or incorporating production costs.
- **Greedy Heuristics and Constructive Methods**: These offer quick, practical solutions, generating an initial arrangement that can be refined using more advanced optimization methods. Common examples include First-Fit Decreasing (FFD) and Best-Fit Decreasing (BFD) heuristics.