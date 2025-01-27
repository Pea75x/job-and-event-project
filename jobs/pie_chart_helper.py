import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64


def get_pie(data, field):
    matplotlib.use('Agg')

    skill_counts = {}
    for job in data:
        for skill in job[field]:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
    
    # Remove skills with only 1 count
    skill_counts = {skill: count for skill, count in skill_counts.items() if count >= 2}

    labels = skill_counts.keys()
    sizes = skill_counts.values()

    fig, ax = plt.subplots()
    colors = ['#f3b0c3','#ecd5e3','#ffc8a2','#97c1a9','#55cbcd', '#d4f0f0', '#ff968a', '#cce2cb', '#fff4bc']
    explode = [0.1] * len(labels)
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, explode=explode)
    ax.axis('equal')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    chart_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return chart_image
