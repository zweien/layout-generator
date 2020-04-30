# 数据格式说明

## mat 文件

`layout_generator` 脚本默认生成 mat 格式数据文件，每个文件存储一组布局数据与对应温度场。可用 `scipy.io.loadmat()` 读取，读取后以字典方式使用，默认 key
- `F`: 布局图像矩阵, `shape = (nx, nx)`
- `u`: 温度场矩阵, `shape = (nx, nx)`
- `list`: (离散布局) 组件所处位置，shape = (unit_n,)
- `xs`: x 坐标矩阵, `shape = (nx, nx)`
- `ys`: y 坐标矩阵, `shape = (nx, nx)`
- `zs`: (3D 布局问题) z 坐标矩阵, `shape = (nx, nx)`

## HDF5 文件

采用 `layout_convert` 可将 `mat` 文件转换成 `HDF5` 文件，采用 index 可访问相应元素