from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
y_true = [0, 1, 1, 1, 0, 1]
y_pred = [0, 1, 0, 1, 0, 1]
accuracy = accuracy_score(y_true, y_pred)
print("Accuracy:", accuracy)
f1 = f1_score(y_true, y_pred)
print("F1 Score:", f1)
recall = recall_score(y_true, y_pred)
print("Recall:", recall)
precision = precision_score(y_true, y_pred)
print("Precision:", precision)
from sklearn.metrics import roc_curve, auc, precision_recall_curve
import matplotlib.pyplot as plt

# 计算ROC曲线的值
fpr, tpr, _ = roc_curve(y_true, y_pred)
roc_auc = auc(fpr, tpr)

# 绘制ROC曲线
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic Example')
plt.legend(loc="lower right")
plt.show()
precision, recall, _ = precision_recall_curve(y_true, y_pred)
auc_score = auc(recall, precision)

# 绘制 Precision-Recall 曲线
plt.figure()
plt.plot(recall, precision, color='blue', label=f'Precision-Recall curve (area = {auc_score:.2f})')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend(loc="lower left")
plt.show()