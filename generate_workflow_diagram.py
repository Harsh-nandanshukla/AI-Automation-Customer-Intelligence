import matplotlib.pyplot as plt

boxes = [
    ("Customer Queries\nInstagram • WhatsApp • Email • Website Chat", 0.5, 0.92),

    ("API / Webhook Layer\nCollect Incoming Messages", 0.5, 0.78),

    ("AI Processing Layer\n• Query Classification\n• Sentiment Detection\n• Priority Assignment", 0.5, 0.64),

    ("Decision Engine\n• Confidence Check\n• Escalation Logic\n• Suggested Reply Generation", 0.5, 0.50),

    ("Data Storage\nQuery Logs • Analytics Dataset", 0.5, 0.36),

    ("Analytics Dashboard\nStreamlit Monitoring & Insights", 0.5, 0.22),

    ("Support Actions\nAuto Reply • Human Escalation", 0.5, 0.08)
]

fig, ax = plt.subplots(figsize=(7,11))

for text, x, y in boxes:
    ax.text(
        x,
        y,
        text,
        ha="center",
        va="center",
        bbox=dict(
            boxstyle="round,pad=0.5",
            fc="#d6eaf8",
            ec="black"
        )
    )

for i in range(len(boxes)-1):
    ax.annotate(
        "",
        xy=(0.5, boxes[i+1][2] + 0.035),
        xytext=(0.5, boxes[i][2] - 0.035),
        arrowprops=dict(
            arrowstyle="->",
            lw=2
        )
    )

ax.set_xlim(0,1)
ax.set_ylim(0,1)
ax.axis("off")

plt.title(
    "AI Customer Support Automation Workflow",
    fontsize=15,
    weight="bold"
)

plt.savefig("workflow_diagram.png", bbox_inches="tight")
print("workflow_diagram.png created successfully")