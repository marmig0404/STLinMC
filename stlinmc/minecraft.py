"""
# minecraft.py
# this module interacts with a Raspberry Juice server
"""

from mcpi import block, connection, minecraft


def build_voxels(voxels, server_ip, server_port=4711):
    """sends build commands for voxels on a server

    Args:
        voxels (np.nDArray[int8]): a set of voxels in a 3D array,
                                   0 and 1 indicate air and block respectively
        server_ip (str): ip of minecraft server running raspberry juice (URL or IPv4)
        server_port (int, optional): server port. defaults to 4711.
    """

    # establish connection to server and get player position
    conn = connection.Connection(server_ip, server_port)
    mc = minecraft.Minecraft(conn)
    try:
        x, y, z = mc.player.getTilePos()
    except connection.RequestError:
        print("No valid player to reference, using (0,0,0)")
        x, y, z = 0, 0, 0

    # set blocks for each voxel
    for layer_index, layer in enumerate(voxels):

        print(f"Sending layer {layer_index+1}/{len(voxels)}... ", end='')
        for row_index, row in enumerate(layer):
            for column_index, column in enumerate(row):
                xc = x + column_index
                yc = y + layer_index
                zc = z + row_index
                if column == 1:
                    mc.setBlock(xc, yc, zc, block.COBBLESTONE.id)
                elif column == 0:
                    mc.setBlock(xc, yc, zc, block.AIR.id)
        print("Sent!")
