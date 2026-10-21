import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = "docs/diagrams/"
C = {"blue":"#2563EB","green":"#059669","orange":"#EA580C","purple":"#7C3AED","gray":"#475569","red":"#DC2626"}

def box(ax, x, y, w, h, text, color, fs=10):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                 fc=color, ec="none"))
    ax.text(x+w/2, y+h/2, text, ha="center", va="center", color="white", fontsize=fs, fontweight="bold", wrap=True)

def arrow(ax, x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2), arrowstyle="-|>", mutation_scale=16, lw=1.8, color="#334155"))

# 1. Workflow flowchart
fig, ax = plt.subplots(figsize=(11, 4.2)); ax.set_xlim(0,11); ax.set_ylim(0,4.2); ax.axis("off")
steps = [("1. Problem\nDefinition",C["blue"]),("2. Data\nCollection",C["green"]),("3. Cleaning &\nPreprocessing",C["orange"]),
         ("4. EDA &\nFeature Eng.",C["purple"]),("5. Modeling",C["blue"]),("6. Evaluation",C["green"]),("7. Report &\nDeployment",C["gray"])]
w, h = 1.3, 1.0
xs = [0.2 + i*1.55 for i in range(7)]
for (t,c),x in zip(steps, xs):
    box(ax, x, 2.4, w, h, t, c, 9)
for i in range(6):
    arrow(ax, xs[i]+w+0.02, 2.9, xs[i+1]-0.02, 2.9)
# feedback loop
ax.annotate("", xy=(xs[3]+w/2, 2.38), xytext=(xs[5]+w/2, 2.38),
            arrowprops=dict(arrowstyle="-|>", lw=1.8, color=C["red"], connectionstyle="arc3,rad=-0.5"))
ax.text(xs[4]+w/2, 1.35, "Iterate: improve features / tune model", ha="center", color=C["red"], fontsize=10, style="italic")
ax.text(5.5, 3.95, "End-to-End Data Science Workflow", ha="center", fontsize=14, fontweight="bold", color="#0F172A")
ax.text(5.5, 0.3, "Python stack: pandas · NumPy · Matplotlib/Seaborn · scikit-learn · XGBoost · Jupyter", ha="center", fontsize=10, color="#334155")
plt.savefig(OUT+"01_workflow.png", dpi=200, bbox_inches="tight"); plt.close()

# 2. Architecture
fig, ax = plt.subplots(figsize=(11, 4.6)); ax.set_xlim(0,11); ax.set_ylim(0,4.6); ax.axis("off")
ax.text(5.5, 4.3, "Project Architecture", ha="center", fontsize=14, fontweight="bold", color="#0F172A")
box(ax, 0.2, 1.8, 1.9, 1.2, "Data Sources\nCSV / SQL / API", C["gray"])
box(ax, 2.6, 1.8, 1.9, 1.2, "Ingestion &\nCleaning\n(pandas)", C["orange"])
box(ax, 5.0, 1.8, 1.9, 1.2, "Feature Store\n(processed\nCSV)", C["purple"])
box(ax, 7.4, 2.7, 1.7, 0.9, "Model Training\nscikit-learn", C["blue"], 9)
box(ax, 7.4, 1.2, 1.7, 0.9, "Evaluation\nMetrics", C["green"], 9)
box(ax, 9.4, 1.8, 1.4, 1.2, "Dashboard /\nReport", C["red"])
arrow(ax,2.12,2.4,2.58,2.4); arrow(ax,4.52,2.4,4.98,2.4)
arrow(ax,6.92,2.6,7.38,3.1); arrow(ax,6.92,2.2,7.38,1.7)
arrow(ax,9.12,3.1,9.38,2.7); arrow(ax,9.12,1.7,9.38,2.1)
ax.text(5.5, 0.5, "Version control: Git + GitHub  |  Environment: Python 3.11 + requirements.txt", ha="center", fontsize=10, color="#334155")
plt.savefig(OUT+"02_architecture.png", dpi=200, bbox_inches="tight"); plt.close()

# 3. Gantt timeline (total 34 hours)
tasks = [("Problem definition & literature review",0,3),("Data collection & understanding",3,7),
         ("Data cleaning & preprocessing",7,12),("Exploratory data analysis",12,18),
         ("Feature engineering",18,22),("Model building & tuning",22,28),
         ("Evaluation & interpretation",28,31),("Documentation & GitHub",31,34)]
cols = [C["blue"],C["green"],C["orange"],C["purple"],C["blue"],C["green"],C["orange"],C["gray"]]
fig, ax = plt.subplots(figsize=(11, 4.6))
for i,((n,s,e),c) in enumerate(zip(tasks,cols)):
    ax.barh(len(tasks)-1-i, e-s, left=s, color=c, height=0.6)
    ax.text(s+(e-s)/2, len(tasks)-1-i, f"{e-s}h", ha="center", va="center", color="white", fontsize=9, fontweight="bold")
ax.set_yticks(range(len(tasks))); ax.set_yticklabels([t[0] for t in tasks][::-1], fontsize=10)
ax.set_xlabel("Cumulative hours"); ax.set_xlim(0,34); ax.grid(axis="x", alpha=0.3)
ax.set_title("Project Timeline (Total: 34 Hours)", fontsize=14, fontweight="bold")
for s in ("top","right"): ax.spines[s].set_visible(False)
plt.savefig(OUT+"03_timeline.png", dpi=200, bbox_inches="tight"); plt.close()

# 4. Methodology pipeline detail
fig, ax = plt.subplots(figsize=(11, 4.4)); ax.set_xlim(0,11); ax.set_ylim(0,4.4); ax.axis("off")
ax.text(5.5, 4.1, "Methodology: Data to Decision Pipeline", ha="center", fontsize=14, fontweight="bold", color="#0F172A")
cols4 = [("Data Cleaning",C["orange"],["Handle missing values","Remove duplicates","Fix data types","Treat outliers"]),
         ("Exploration",C["purple"],["Churn distribution","Correlation heatmap","Tenure vs churn","Contract analysis"]),
         ("Modeling",C["blue"],["Logistic Regression","Random Forest","XGBoost","SMOTE for imbalance"]),
         ("Evaluation",C["green"],["Precision / Recall","F1 & ROC-AUC","Confusion matrix","5-fold CV"])]
for i,(t,c,items) in enumerate(cols4):
    x = 0.2 + i*2.7
    box(ax, x, 3.0, 2.4, 0.7, t, c, 11)
    for j,it in enumerate(items):
        ax.add_patch(FancyBboxPatch((x, 2.3-j*0.6), 2.4, 0.46, boxstyle="round,pad=0.02,rounding_size=0.08", fc="#F1F5F9", ec=c, lw=1.5))
        ax.text(x+1.2, 2.53-j*0.6, it, ha="center", va="center", fontsize=9, color="#0F172A")
    if i<3: arrow(ax, x+2.42, 3.35, x+2.68, 3.35)
plt.savefig(OUT+"04_methodology.png", dpi=200, bbox_inches="tight"); plt.close()
print("ok")
