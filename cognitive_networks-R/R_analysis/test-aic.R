# 设置工作目录到包含np_0.20-0.tar.gz的文件夹
setwd("D:/cognitive_networks-main/cognitive_networks-R")
# 从本地安装np包
install.packages("np_0.20-0.tar.gz", repos = NULL, type = "source")
# 安装包
install.packages("ggplot2")
install.packages("gridExtra")
#########################################################(以上为首次运行需要)


# 加载包
library(np)
library(ggplot2)
library(gridExtra)

# 设置工作目录到包含数据文件的文件夹
setwd("D:/cognitive_networks-main/cognitive_networks-R")

# 导入数据(从词汇数量2~8中的一个)
number = 8
data <- read.csv(sprintf("R_data/06-merge-T_ij-w_iw_j-s-d-final-%s.csv", number))

# 计算 W_ij 和 W_ij / D_ij  (选择合适的特征变量)
data$W_ij <- data$eigenvector_centrality_i * data$eigenvector_centrality_j
data$W_ij_D_ij_ratio <- data$W_ij / data$shortest_path_length

# 设置因变量和自变量
T_ij <- data$num_paths
W_ij <- data$W_ij
D_ij <- data$shortest_path_length
W_ij_D_ij_ratio <- data$W_ij_D_ij_ratio

# 选择带宽(cv.aic)
bw1 <- npregbw(T_ij ~ W_ij, regtype = "ll", bwmethod = "cv.aic")
bw2 <- npregbw(T_ij ~ D_ij, regtype = "ll", bwmethod = "cv.aic")
bw3 <- npregbw(T_ij ~ W_ij_D_ij_ratio, regtype = "ll", bwmethod = "cv.aic")

# 设置输出文件名
output_file <- sprintf("R_results/Output_aic_Network_%s.txt", number)

# 重定向输出到txt文件
sink(output_file)

# 使用summary函数查看带宽选择的详细信息
print("Bandwidth Selection Summary:")
print(summary(bw1))
print(summary(bw2))
print(summary(bw3))

# 非参数估计
model1 <- npreg(bws = bw1, data = data.frame(T_ij = T_ij, W_ij = W_ij))
model2 <- npreg(bws = bw2, data = data.frame(T_ij = T_ij, D_ij = D_ij))
model3 <- npreg(bws = bw3, data = data.frame(T_ij = T_ij, W_ij_D_ij_ratio = W_ij_D_ij_ratio))

# 提取拟合值和置信区间
fit1 <- predict(model1, newdata = data.frame(W_ij = W_ij), se.fit = TRUE)
fit2 <- predict(model2, newdata = data.frame(D_ij = D_ij), se.fit = TRUE)
fit3 <- predict(model3, newdata = data.frame(W_ij_D_ij_ratio = W_ij_D_ij_ratio), se.fit = TRUE)

# 创建数据框用于绘图
plot_data1 <- data.frame(W_ij = W_ij, T_ij = T_ij, fit = fit1$fit, se = fit1$se.fit)
plot_data2 <- data.frame(D_ij = D_ij, T_ij = T_ij, fit = fit2$fit, se = fit2$se.fit)
plot_data3 <- data.frame(W_ij_D_ij_ratio = W_ij_D_ij_ratio, T_ij = T_ij, fit = fit3$fit, se = fit3$se.fit)

# 绘制图形1: T_ij vs W_ij
p1 <- ggplot(plot_data1, aes(x = W_ij, y = T_ij)) +
  geom_point(alpha = 0.5, color = "black", fill = "black") +
  geom_line(aes(y = fit), color = "blue") +
  geom_ribbon(aes(ymin = fit - 1.96 * se, ymax = fit + 1.96 * se), alpha = 0.2) +
  scale_x_log10(sec.axis = dup_axis(labels = NULL, name = NULL)) +
  scale_y_log10(sec.axis = dup_axis(labels = NULL, name = NULL)) +
  labs(x = expression(log(W[i] * W[j])), y = expression(log(T[ij]))) +
  theme_minimal() +
  theme(
    panel.border = element_rect(color = "black", fill = NA, linewidth = 1),
    axis.line = element_line(color = "black"),
    axis.ticks.length = unit(-0.1, "cm"),  # 负值使刻度线朝向内部
    axis.ticks = element_line(color = "black"),
    axis.text.x = element_text(margin = margin(t = 5, r = 5, b = 5, l = 5)),
    axis.text.y = element_text(margin = margin(t = 5, r = 5, b = 5, l = 5)),
    axis.ticks.x.top = element_line(color = "black"),  # 最上边框线的刻度线
    axis.ticks.y.right = element_line(color = "black")  # 最右边框线的刻度线
  )

# 绘制图形2: T_ij vs D_ij
p2 <- ggplot(plot_data2, aes(x = D_ij, y = T_ij)) +
  geom_point(alpha = 0.5) +
  geom_line(aes(y = fit), color = "blue") +
  geom_ribbon(aes(ymin = fit - 1.96 * se, ymax = fit + 1.96 * se), alpha = 0.2) +
  scale_x_log10(sec.axis = dup_axis(labels = NULL, name = NULL)) +
  scale_y_log10(sec.axis = dup_axis(labels = NULL, name = NULL)) +
  labs(x = expression(log(D[ij])), y = expression(log(T[ij]))) +
  theme_minimal() +
  theme(
    panel.border = element_rect(color = "black", fill = NA, linewidth = 1),
    axis.line = element_line(color = "black"),
    axis.ticks.length = unit(-0.1, "cm"),  # 负值使刻度线朝向内部
    axis.ticks = element_line(color = "black"),
    axis.text.x = element_text(margin = margin(t = 5, r = 5, b = 5, l = 5)),
    axis.text.y = element_text(margin = margin(t = 5, r = 5, b = 5, l = 5)),
    axis.ticks.x.top = element_line(color = "black"),  # 最上边框线的刻度线
    axis.ticks.y.right = element_line(color = "black")  # 最右边框线的刻度线
  )

# 绘制图形3: T_ij vs W_ij / D_ij
p3 <- ggplot(plot_data3, aes(x = W_ij_D_ij_ratio, y = T_ij)) +
  geom_point(alpha = 0.5) +
  geom_line(aes(y = fit), color = "blue") +
  geom_ribbon(aes(ymin = fit - 1.96 * se, ymax = fit + 1.96 * se), alpha = 0.2) +
  scale_x_log10(sec.axis = dup_axis(labels = NULL, name = NULL)) +
  scale_y_log10(sec.axis = dup_axis(labels = NULL, name = NULL)) +
  labs(x = expression(log(W[i] * W[j] / D[ij])), y = expression(log(T[ij]))) +
  theme_minimal() +
  theme(
    panel.border = element_rect(color = "black", fill = NA, linewidth = 1),
    axis.line = element_line(color = "black"),
    axis.ticks.length = unit(-0.1, "cm"),  # 负值使刻度线朝向内部
    axis.ticks = element_line(color = "black"),
    axis.text.x = element_text(margin = margin(t = 5, r = 5, b = 5, l = 5)),
    axis.text.y = element_text(margin = margin(t = 5, r = 5, b = 5, l = 5)),
    axis.ticks.x.top = element_line(color = "black"),  # 最上边框线的刻度线
    axis.ticks.y.right = element_line(color = "black")  # 最右边框线的刻度线
  )

# 打印模型评估输出
cat("\nModel 1:\n")
print(summary(model1))
cat("\nModel 2:\n")
print(summary(model2))
cat("\nModel 3:\n")
print(summary(model3))

# 停止重定向
sink()

# 设置图片大小
single_plot_height <- 7.08661 / 1.5
total_height <- single_plot_height * 3
# 整合图形并显示
p_combined <- grid.arrange(p1, p2, p3, ncol = 1)
# 保存图形为文件
ggsave(sprintf("R_results/Fig_aic_Network_%s_all.jpeg", number), p_combined, width = 7.08661, height = total_height, units = "in", dpi = 300)

# 保存图像，宽度为 180 mm (7.08661 inches)，分辨率为 300 dpi
ggsave(sprintf("R_results/Fig_aic_Network_%s_p1.jpeg", number), p1, width = 7.08661, height = 7.08661 / 1.5, units = "in", dpi = 300)
ggsave(sprintf("R_results/Fig_aic_Network_%s_p2.jpeg", number), p2, width = 7.08661, height = 7.08661 / 1.5, units = "in", dpi = 300)
ggsave(sprintf("R_results/Fig_aic_Network_%s_p3.jpeg", number), p3, width = 7.08661, height = 7.08661 / 1.5, units = "in", dpi = 300)
