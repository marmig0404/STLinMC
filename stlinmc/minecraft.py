from mcpi import block, connection, minecraft
from .voxel import import_stl_as_voxels


def build_voxels(voxels, server_ip, server_port=4711):

    conn = connection.Connection(server_ip, server_port)
    mc = minecraft.Minecraft(conn)
    try:
        x, y, z = mc.player.getTilePos()
    except connection.RequestError:
        print("No valid player to reference, using (0,0,0)")
        x, y, z = 0, 0, 0
    for layer_index, layer in enumerate(voxels):
        for row_index, row in enumerate(layer):
            for column_index, column in enumerate(row):
                xc = x+column_index
                yc = y + layer_index
                zc = z + row_index
                if column == 1:
                    mc.setBlock(xc, yc, zc, block.COBBLESTONE.id)
                else:
                    mc.setBlock(xc, yc, zc, block.AIR.id)
