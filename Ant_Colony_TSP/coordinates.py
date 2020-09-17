import math

coordinates = [[1150,1760],
[630,1660],
[40,2090],
[750,1100],
[750,2030],
[1030,2070],
[1650,650],
[1490,1630],
[790,2260],
[710,1310],
[840,550],
[1170,2300],
[970,1340],
[510,700],
[750,900],
[1280,1200],
[230,590],
[460,860],
[1040,950],
[590,1390],
[830,1770],
[490,500],
[1840,1240],
[1260,1500],
[1280,790],
[490,2130],
[1460,1420],
[1260,1910],
[360,1980]]

# distance  = []
# Below was code used to create the distance array
# i = 1
# for start in coordinates:
#     j = 1
#     new = []
#     for end in coordinates:
#         if start == end:
#             foo = 0
#         else:
#             foo = math.sqrt(pow(end[0]-start[0],2)+
#                                         pow(end[1]-start[1],2))
#         new.append(foo)
#         j = j + 1
#     distance.append(new)
#     i = i + 1

distances = [[0, 529.5280917949491, 1158.015543937127, 771.7512552629895, 482.59714048054616, 332.41540277189324, 1217.4152947946727, 364.0054944640259, 616.1168720299745, 629.3647591023825, 1249.0796611905903, 540.3702434442519, 456.9463863518345, 1238.2245353731284, 948.4724561103501, 574.8912940721924, 1488.388390172404, 1134.063490286148, 817.4350127074323, 
671.1929677819934, 320.1562118716424, 1422.3923509355639, 864.002314811714, 282.3118842698621, 978.6725703727473, 756.6372975210778, 460.10868281309365, 186.01075237738274, 820.0609733428363], [529.5280917949491, 0, 730.0684899377592, 572.7128425310541, 388.9730067755345, 572.8001396647875, 1435.4441821262155, 860.5230967266364, 620.966987850401, 359.02646142032484, 1129.6902230257638, 837.3768566183329, 466.9047011971501, 967.470929795826, 769.4153624668538, 796.3039620647382, 1142.322196230118, 817.8630692236935, 819.8780397107853, 272.9468812791236, 228.25424421026653, 1168.4177335182824, 1280.8200498118383, 650.0, 1086.0018416190646, 490.40799340956914, 864.002314811714, 677.7905281132217, 418.68842830916645], [1158.015543937127, 730.0684899377592, 0, 1218.2774724995943, 712.5307010929424, 990.2019995940223, 2160.023148024113, 1521.2166183683375, 769.0253571892152, 1028.2509421342631, 1735.396208362805, 1149.3476410555686, 1194.7384651043926, 1467.310464761974, 1385.712812959453, 1526.3354808167173, 1511.985449665439, 1299.7307413460683, 1516.443206981389, 890.2246907382428, 852.3496934944014, 1652.4527224704493, 1990.6029237394382, 1355.1752654177244, 1796.5522536235899, 451.7742799230607, 1570.1273833673497, 1233.2072007574395, 338.3784863137726], [771.7512552629895, 572.7128425310541, 1218.2774724995943, 0, 930.0, 1009.603882718366, 1006.2305898749054, 910.2197536858888, 1160.6894502837526, 213.7755832643195, 557.3149917237109, 1271.3772060250255, 325.5764119219941, 466.47615158762403, 200.0, 539.351462406472, 728.3543093852057, 376.4306044943742, 326.49655434629017, 331.2099032335839, 674.7592163134935, 653.9113089708726, 1098.9540481748998, 648.1512169239521, 614.00325732035, 1062.308806327049, 778.7810988975015, 957.183368012629, 962.5487000666511], [482.59714048054616, 388.9730067755345, 712.5307010929424, 930.0, 0, 282.842712474619, 1647.5436261295176, 841.1896337925236, 233.45235059857504, 
721.1102550927978, 1482.7339613025663, 499.29950931279717, 724.2237223399962, 1351.4806694880988, 1130.0, 984.7842403288143, 1531.012736720371, 1205.404496424333, 1118.257573191436, 659.6969000988257, 272.02941017470886, 1551.9342769589182, 1346.1797799699712, 735.5270219373317, 1348.517704741024, 278.5677655436824, 936.055553906925, 523.9274758971894, 393.19206502675], [332.41540277189324, 572.8001396647875, 990.2019995940223, 1009.603882718366, 282.842712474619, 0, 1549.451515859725, 636.5532185135819, 306.10455730027934, 824.6211251235321, 1531.8289721767244, 269.2582403567252, 732.4616030891995, 1465.3668482670132, 1203.0378215168466, 905.2071586106686, 1682.3792675850473, 1337.5350462698163, 1120.0446419674531, 809.9382692526635, 360.5551275463989, 1660.2710622064096, 1159.7413504743201, 614.6543744251724, 1304.1855696180662, 543.323108288245, 779.3587107359486, 
280.178514522438, 676.0177512462228], [1217.4152947946727, 1435.4441821262155, 2160.023148024113, 1006.2305898749054, 1647.5436261295176, 1549.451515859725, 0, 992.9753269845128, 1825.2944967867513, 1148.5643212288983, 816.1494961096282, 1718.4004189943623, 968.7620966986683, 1141.0959644131601, 934.0770846134702, 662.872536767062, 1421.2670403551895, 1208.3873551142449, 679.7793759742935, 1292.749008895385, 1388.0922159568506, 1169.6580696938743, 619.8386886924694, 935.200513259055, 395.60080889704966, 1880.4254837669052, 793.095202355934, 1318.9768762188364, 1852.8356645962965], [364.0054944640259, 860.5230967266364, 1521.2166183683375, 910.2197536858888, 841.1896337925236, 636.5532185135819, 
992.9753269845128, 0, 941.7536832951597, 843.0895563343197, 1260.5157674539419, 742.4957912338629, 595.3990258641678, 1351.0366390294528, 1039.471019317037, 478.53944456021594, 1633.768649472746, 1286.0015552090128, 815.4140052758476, 931.4504817756015, 674.68511173732, 1508.9400253157844, 524.0229002629561, 264.1968962724581, 865.8521813797087, 1118.033988749895, 212.13203435596427, 362.3534186398688, 1182.9623831720094], [616.1168720299745, 620.966987850401, 769.0253571892152, 1160.6894502837526, 233.45235059857504, 306.10455730027934, 1825.2944967867513, 941.7536832951597, 0, 953.3624704172071, 1710.7308379753958, 382.099463490856, 937.4433316206372, 1584.9290204927158, 1360.5881081355958, 1167.7756633874505, 1761.3914953808537, 1438.3671297690307, 1333.641631023867, 892.6925562588724, 491.62994213127416, 1785.3851125177448, 1463.8647478507023, 893.5882720806043, 1549.5160534825059, 326.9556544854363, 1074.476616776745, 586.0034129593445, 513.1276644267], [629.3647591023825, 359.02646142032484, 1028.2509421342631, 213.7755832643195, 721.1102550927978, 824.6211251235321, 1148.5643212288983, 843.0895563343197, 953.3624704172071, 0, 771.0382610480494, 1091.6501271011698, 261.72504656604804, 641.9501538281613, 411.9465984809196, 580.5170109479997, 865.3323061113574, 514.78150704935, 488.3646178829912, 144.22205101855957, 475.3945729601885, 839.3449827097318, 1132.1660655575224, 581.8934610390462, 771.5568676384133, 848.999411071645, 758.023746329889, 813.9410298049853, 755.9100475585703], [1249.0796611905903, 1129.6902230257638, 1735.396208362805, 557.3149917237109, 1482.7339613025663, 1531.8289721767244, 816.1494961096282, 1260.5157674539419, 1710.7308379753958, 771.0382610480494, 0, 1780.8424972467385, 800.6247560499238, 362.49137920783716, 361.386219991853, 784.9203781276162, 611.310068623117, 490.40799340956914, 447.21359549995793, 876.4131445842195, 1220.040982918197, 353.5533905932738, 1214.9485585818027, 1038.7011119662866, 501.1985634456667, 1618.3015788165073, 1068.3164325236226, 1423.3762678926469, 1508.409758653132], [540.3702434442519, 837.3768566183329, 1149.3476410555686, 1271.3772060250255, 499.29950931279717, 269.2582403567252, 1718.4004189943623, 742.4957912338629, 382.099463490856, 1091.6501271011698, 1780.8424972467385, 0, 980.612053770501, 1730.7801709055948, 1461.642911247477, 1105.4863183232978, 1951.3328778042971, 1605.5217220579732, 1356.244815658294, 1079.1200118615168, 629.6824596572466, 1924.162155328911, 1253.9936203984453, 805.0465825031494, 1514.0013210033867, 700.9279563550023, 926.5527507918802, 400.24992192379, 870.9190547921202], [456.9463863518345, 466.9047011971501, 1194.7384651043926, 325.5764119219941, 724.2237223399962, 732.4616030891995, 968.7620966986683, 595.3990258641678, 937.4433316206372, 261.72504656604804, 800.6247560499238, 980.612053770501, 0, 788.1624198095212, 491.9349550499537, 340.14702703389895, 1053.612832116238, 700.3570517957252, 396.23225512317896, 383.275357934736, 452.21676218380054, 967.470929795826, 875.7282683572571, 331.2099032335839, 631.3477647065839, 924.3916918709298, 496.4876634922564, 639.5310782127792, 884.1379982785493], [1238.2245353731284, 967.470929795826, 1467.310464761974, 466.47615158762403, 1351.4806694880988, 1465.3668482670132, 1141.0959644131601, 1351.0366390294528, 1584.9290204927158, 641.9501538281613, 362.49137920783716, 1730.7801709055948, 788.1624198095212, 0, 312.40998703626616, 918.0958555619343, 300.83217912982644, 167.6305461424021, 586.0034129593445, 694.6221994724903, 1116.8258592994703, 200.9975124224178, 1435.4441821262155, 1096.5856099730654, 775.2418977325723, 1430.139853301068, 1192.015100575492, 1423.5870187663274, 1288.7590930814029], [948.4724561103501, 769.4153624668538, 1385.712812959453, 200.0, 1130.0, 1203.0378215168466, 934.0770846134702, 1039.471019317037, 1360.5881081355958, 411.9465984809196, 361.386219991853, 1461.642911247477, 491.9349550499537, 312.40998703626616, 0, 609.0155991434045, 605.3924347066124, 292.7456233660889, 294.27877939124323, 515.4609587543949, 873.6704184073077, 477.07441767506253, 1141.7968295629482, 787.4642849044012, 541.2947441089743, 1257.179382586272, 880.056816347672, 1131.4592347937241, 1148.2595525402783], [574.8912940721924, 796.3039620647382, 1526.3354808167173, 539.351462406472, 984.7842403288143, 905.2071586106686, 662.872536767062, 478.53944456021594, 1167.7756633874505, 580.5170109479997, 784.9203781276162, 1105.4863183232978, 340.14702703389895, 918.0958555619343, 609.0155991434045, 0, 1214.3310915891102, 887.6936408468858, 346.5544690232691, 715.6814934033156, 726.2231062146122, 1055.5093557141026, 561.426753904728, 300.66592756745814, 410.0, 1220.2458768625281, 284.2534080710379, 710.2816342831906, 1206.1509026651681], 
[1488.388390172404, 1142.322196230118, 1511.985449665439, 728.3543093852057, 1531.012736720371, 1682.3792675850473, 1421.2670403551895, 1633.768649472746, 1761.3914953808537, 865.3323061113574, 611.310068623117, 1951.3328778042971, 1053.612832116238, 300.83217912982644, 605.3924347066124, 1214.3310915891102, 0, 354.682957019364, 886.3972021616494, 877.2684879784523, 1323.782459469833, 275.13632984395207, 1736.2603491412226, 1374.4089638822936, 1068.8779163215975, 1561.793840428371, 1483.846353232032, 1674.3058263053379, 1396.0659010233005], [1134.063490286148, 817.8630692236935, 1299.7307413460683, 376.4306044943742, 1205.404496424333, 1337.5350462698163, 1208.3873551142449, 1286.0015552090128, 
1438.3671297690307, 514.78150704935, 490.40799340956914, 1605.5217220579732, 700.3570517957252, 167.6305461424021, 292.7456233660889, 887.6936408468858, 354.682957019364, 0, 586.9412236331675, 545.7105459856901, 982.344135219425, 361.24783736376884, 1431.3629868066312, 1024.4998779892558, 822.9823813423955, 1270.3542812932146, 1146.1239025515522, 1320.0378782444086, 1124.4554237496477], [817.4350127074323, 819.8780397107853, 1516.443206981389, 326.49655434629017, 1118.257573191436, 1120.0446419674531, 679.7793759742935, 815.4140052758476, 1333.641631023867, 488.3646178829912, 447.21359549995793, 1356.244815658294, 396.23225512317896, 586.0034129593445, 294.27877939124323, 346.5544690232691, 886.3972021616494, 586.9412236331675, 0, 629.3647591023825, 846.4632301523794, 710.6335201775947, 850.9406559801923, 592.3681287847954, 288.44410203711914, 1301.8832512940628, 630.3173803727769, 984.8857801796105, 1234.220401711137], [671.1929677819934, 272.9468812791236, 890.2246907382428, 331.2099032335839, 659.6969000988257, 809.9382692526635, 1292.749008895385, 931.4504817756015, 892.6925562588724, 144.22205101855957, 876.4131445842195, 1079.1200118615168, 383.275357934736, 694.6221994724903, 515.4609587543949, 715.6814934033156, 877.2684879784523, 545.7105459856901, 629.3647591023825, 0, 449.44410108488466, 
895.6003573022958, 1258.967831201417, 678.9698078707182, 914.3850392476902, 746.7261881037788, 870.5170877128145, 848.1155581640983, 633.2456079595025], [320.1562118716424, 228.25424421026653, 852.3496934944014, 674.7592163134935, 272.02941017470886, 360.5551275463989, 1388.0922159568506, 674.68511173732, 491.62994213127416, 475.3945729601885, 1220.040982918197, 629.6824596572466, 452.21676218380054, 1116.8258592994703, 873.6704184073077, 726.2231062146122, 1323.782459469833, 982.344135219425, 846.4632301523794, 449.44410108488466, 0, 1314.7243057006285, 1140.6138698087095, 507.74009099144416, 1078.3784122468328, 495.17673612559787, 720.69410986909, 452.21676218380054, 514.78150704935], [1422.3923509355639, 1168.4177335182824, 1652.4527224704493, 653.9113089708726, 1551.9342769589182, 1660.2710622064096, 1169.6580696938743, 1508.9400253157844, 1785.3851125177448, 839.3449827097318, 353.5533905932738, 1924.162155328911, 967.470929795826, 200.9975124224178, 477.07441767506253, 1055.5093557141026, 275.13632984395207, 361.24783736376884, 710.6335201775947, 895.6003573022958, 1314.7243057006285, 0, 1539.5129099815954, 1262.1014222319852, 841.5461959987699, 1630.0, 1336.899397860587, 1606.5490966665163, 1485.6984889270097], [864.002314811714, 1280.8200498118383, 1990.6029237394382, 1098.9540481748998, 1346.1797799699712, 1159.7413504743201, 619.8386886924694, 524.0229002629561, 1463.8647478507023, 1132.1660655575224, 1214.9485585818027, 1253.9936203984453, 875.7282683572571, 1435.4441821262155, 1141.7968295629482, 561.426753904728, 1736.2603491412226, 1431.3629868066312, 850.9406559801923, 1258.967831201417, 1140.6138698087095, 1539.5129099815954, 0, 635.6099432828281, 718.4010022264724, 1616.9724796668618, 420.47592083257274, 886.1715409558129, 1654.6903033498443], [282.3118842698621, 650.0, 1355.1752654177244, 648.1512169239521, 735.5270219373317, 614.6543744251724, 935.200513259055, 264.1968962724581, 893.5882720806043, 581.8934610390462, 1038.7011119662866, 805.0465825031494, 331.2099032335839, 1096.5856099730654, 787.4642849044012, 300.66592756745814, 1374.4089638822936, 1024.4998779892558, 592.3681287847954, 678.9698078707182, 507.74009099144416, 1262.1014222319852, 635.6099432828281, 0, 710.2816342831906, 994.8869282486327, 215.40659228538016, 410.0, 1020.0], [978.6725703727473, 1086.0018416190646, 1796.5522536235899, 614.00325732035, 1348.517704741024, 1304.1855696180662, 395.60080889704966, 865.8521813797087, 1549.5160534825059, 771.5568676384133, 501.1985634456667, 1514.0013210033867, 631.3477647065839, 775.2418977325723, 541.2947441089743, 410.0, 1068.8779163215975, 822.9823813423955, 288.44410203711914, 914.3850392476902, 1078.3784122468328, 841.5461959987699, 718.4010022264724, 710.2816342831906, 0, 1555.538491969903, 655.2098900352466, 1120.1785571952357, 1504.1608956491323], [756.6372975210778, 490.40799340956914, 451.7742799230607, 1062.308806327049, 278.5677655436824, 543.323108288245, 1880.4254837669052, 1118.033988749895, 326.9556544854363, 848.999411071645, 1618.3015788165073, 700.9279563550023, 924.3916918709298, 1430.139853301068, 1257.179382586272, 1220.2458768625281, 1561.793840428371, 1270.3542812932146, 1301.8832512940628, 746.7261881037788, 495.17673612559787, 1630.0, 1616.9724796668618, 994.8869282486327, 1555.538491969903, 0, 1202.0815280171307, 800.812087820857, 198.4943324127921], [460.10868281309365, 864.002314811714, 1570.1273833673497, 778.7810988975015, 936.055553906925, 779.3587107359486, 793.095202355934, 212.13203435596427, 
1074.476616776745, 758.023746329889, 1068.3164325236226, 926.5527507918802, 496.4876634922564, 1192.015100575492, 880.056816347672, 284.2534080710379, 1483.846353232032, 1146.1239025515522, 630.3173803727769, 870.5170877128145, 720.69410986909, 1336.899397860587, 
420.47592083257274, 215.40659228538016, 655.2098900352466, 1202.0815280171307, 0, 529.2447448959697, 1234.3419299367579], [186.01075237738274, 677.7905281132217, 1233.2072007574395, 957.183368012629, 523.9274758971894, 280.178514522438, 1318.9768762188364, 362.3534186398688, 586.0034129593445, 813.9410298049853, 1423.3762678926469, 400.24992192379, 639.5310782127792, 1423.5870187663274, 1131.4592347937241, 710.2816342831906, 1674.3058263053379, 1320.0378782444086, 984.8857801796105, 848.1155581640983, 452.21676218380054, 1606.5490966665163, 886.1715409558129, 410.0, 1120.1785571952357, 800.812087820857, 529.2447448959697, 0, 902.7181176868004], [820.0609733428363, 418.68842830916645, 338.3784863137726, 962.5487000666511, 393.19206502675, 676.0177512462228, 1852.8356645962965, 1182.9623831720094, 513.1276644267, 755.9100475585703, 1508.409758653132, 870.9190547921202, 
884.1379982785493, 1288.7590930814029, 1148.2595525402783, 1206.1509026651681, 1396.0659010233005, 1124.4554237496477, 1234.220401711137, 633.2456079595025, 514.78150704935, 1485.6984889270097, 1654.6903033498443, 1020.0, 1504.1608956491323, 198.4943324127921, 1234.3419299367579, 902.7181176868004, 0]]

# sum = 0
# for val in distances[0]:
#     if val != 0:    
#         sum = sum + 1/val

# print (sum)

def calculate_cost(path):
    sum = 0
    for i in range (0,path.__len__()):
        if i == path.__len__() - 1:
            sum = sum + distances[path[i]][path[0]]
        else:
            sum = sum + distances[path[i]][path[(i+1)]]
    return sum


if __name__ == "__main__":
    path = [8, 4, 20, 1, 19, 9, 3, 14, 17, 13, 21, 16, 10, 18, 24, 6, 22, 26, 23, 7, 27, 0, 5, 11, 25, 28, 2, 12, 15]
    path1 = [26, 7, 1, 20, 9, 19, 3, 18, 24, 6, 22, 23, 0, 27, 5, 11, 8, 28, 4, 25, 2, 12, 15, 14, 17, 13, 21, 10, 16]
    path2 = [8, 4, 20, 1, 19, 9, 3, 14, 17, 13, 21, 16, 10, 18, 24, 6, 22, 26, 7, 0, 23, 12, 15, 28, 25, 2, 27, 5, 11]
    path3 = [12, 9, 19, 1, 20, 0, 27, 5, 11, 8, 4, 25, 28, 2, 3, 14, 17, 13, 21, 16, 10, 18, 15, 24, 6, 22, 26, 7, 23]

    path4 = [20, 1, 19, 9, 3, 14, 17, 13, 16, 21, 10, 18, 24, 6, 22, 7, 26, 15, 12, 23, 0, 27, 5, 11, 8, 25, 2, 28, 4]
    path5 = [1,28,6,12,9,5,26,29,3,2,20,10,4,15,18,17,14,22,11,19,25,7,23,27,8,24,16,13,21]
    path6 = [i-1 for i in path5]

    cost = calculate_cost(path6)
    print (cost)