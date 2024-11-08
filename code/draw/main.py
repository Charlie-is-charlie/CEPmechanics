import os
import matplotlib.pyplot as plt
import argparse
import numpy as np

# 设置默认字体为 Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 自定义一个参数解析器
parser = argparse.ArgumentParser()
# 设置输出结果的文件路径
parser.add_argument('-op', '--output_path', help='Output path (default ./file_name)', type=str, nargs=1,
                    default=['output'])
# 设置输出结果的文件前缀
parser.add_argument('-of', '--output_prefix', help='Output path (default res**)', type=str, nargs=1, default=['res'])

# 设置绘图时 X 方向上的节点数量
parser.add_argument('-nxp', '--num_x', help='Num Node in X for plotting final results (default 200)', type=int,
                    nargs=1, default=[200])
# 设置绘图时 Y 方向上的节点数量
parser.add_argument('-nyp', '--num_y', help='Num Node in Y for plotting final results (default 200)', type=int,
                    nargs=1, default=[200])

args = parser.parse_args()
q = 4  # N/mm
l = 4000.0  # mm
h = 1000.0  # mm

X_mesh_plot = np.linspace(-2000, 2000, args.num_x[0]).reshape((-1, 1))
Y_mesh_plot = np.linspace(-500, 500, args.num_y[0]).reshape((-1, 1))
X_plot, Y_plot = np.meshgrid(X_mesh_plot, Y_mesh_plot)
input_plot = [X_plot.reshape(-1, 1), Y_plot.reshape(-1, 1)]
np.savetxt("X_mesh", X_plot, delimiter=', ')
np.savetxt("Y_mesh", Y_plot, delimiter=', ')

if not os.path.isdir(args.output_path[0]):
    os.mkdir(args.output_path[0])


def stress_x(xx):
    x, y = xx[0], xx[1]
    return -(6 * q / h ** 3) * x ** 2 * y + 4 * q / h ** 3 * y ** 3 + (
            3 * q * l ** 2 / (2 * h ** 3) - 3 * q / (5 * h)) * y


def stress_y(xx):
    x, y = xx[0], xx[1]
    return -2 * q * y ** 3 / h ** 3 + 3 * q * y / (2 * h) - q / 2


def stress_xy(xx):
    x, y = xx[0], xx[1]
    return (6 * q / h ** 3) * x * y ** 2 - (3 * q / (2 * h) * x)


def cust_pcolor(AX, X, Y, C, title):
    im = AX.pcolor(X, Y, C, cmap="jet", shading='auto')
    AX.axis("equal")
    AX.axis("off")  # 关闭坐标轴的显示
    AX.set_ylim(AX.get_ylim()[::-1])  # 反转y轴
    AX.set_title(title, fontsize=24)
    # 颜色条在下方，适当调整长度
    cbar = plt.colorbar(im, ax=AX, orientation='horizontal', pad=0, aspect=30)
    cbar.set_label("(MPa)", fontsize=16)
    cbar.ax.tick_params(labelsize=16)

    # cbar.set_label(f"{title} (单位: MPa)", fontsize=14, fontname='Times New Roman')  # 设置标题与单位


def plot():
    output_file_name = os.path.join(args.output_path[0], args.output_prefix[0])
    X = np.loadtxt("X_mesh", delimiter=',')
    Y = np.loadtxt("Y_mesh", delimiter=',')
    # Stress可视化
    fig, ax = plt.subplots(1, 3, figsize=(15, 3), dpi=300)
    cust_pcolor(ax[0], X, Y, stress_x([X, Y]), "Sx")
    cust_pcolor(ax[1], X, Y, stress_y([X, Y]), "Sy")
    cust_pcolor(ax[2], X, Y, stress_xy([X, Y]), "Sxy")
    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.2, top=0.7, wspace=0.3)
    plt.savefig("{}_Stress.png".format(output_file_name))
    try:
        plt.savefig("{}_Stress.png".format(output_file_name))
    except FileNotFoundError:
        print("Error: Output directory does not exist or is not writable.")


if __name__ == "__main__":
    plot()
