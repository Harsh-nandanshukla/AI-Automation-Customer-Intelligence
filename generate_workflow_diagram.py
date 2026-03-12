import matplotlib.pyplot as plt

boxes = [
    ("Customer Messages\n(Instagram / WhatsApp / Email)", 0.5, 0.9),
    ("API / Webhook\nData Ingestion", 0.5, 0.75),
    ("AI Processing Layer\n• Query Classification\n• Sentiment Detection", 0.5, 0.6),
    ("Automation Engine\n• Auto Replies\n• Escalation Logic", 0.5, 0.45),
    ("Data Storage\nQuery Logs & Analytics", 0.5, 0.3),
    ("Analytics Dashboard\n(Streamlit)", 0.5, 0.15),
]

fig, ax = plt.subplots(figsize=(6,10))

for text, x, y in boxes:
    ax.text(
        x, y, text,
        ha='center', va='center',
        bbox=dict(boxstyle="round,pad=0.4", fc="lightblue", ec="black")
    )

for i in range(len(boxes)-1):
    ax.annotate(
        "",
        xy=(0.5, boxes[i+1][2]+0.03),
        xytext=(0.5, boxes[i][2]-0.03),
        arrowprops=dict(arrowstyle="->", lw=2)
    )

ax.set_xlim(0,1)
ax.set_ylim(0,1)
ax.axis('off')

plt.title("AI Customer Support Automation Workflow", fontsize=14)

plt.savefig("workflow_diagram.png", bbox_inches="tight")
print("workflow_diagram.png created successfully")