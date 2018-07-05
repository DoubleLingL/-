option = {
    title: {
        text: '2016/09/07 Flow',
        subtext: '23142'
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: ['InFlow', 'OutFlow', 'Flow']
    },
    toolbox: {
        show: true,
        feature: {
            mark: {show: true},
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore: {show: true},
            saveAsImage: {show: true}
        }
    },
    calculable: true,
    xAxis: [
        {
            type: 'category',
            boundaryGap: false,
            data: ['00:00', '01:00', '02:00', '03:00', '04:00',
                   '05:00', '06:00', '07:00', '08:00', '09:00',
                   '10:00', '11:00', '12:00', '13:00', '14:00',
                   '15:00', '16:00', '17:00', '18:00', '19:00',
                   '20:00', '21:00', '22:00', '23:00']
        }
    ],
    yAxis: [
        {
            type: 'value',
            axisLabel: {
                formatter: '{value} '
            }
        }
    ],
    series: [
        {
            name: 'seqGridInFlow',
            type: 'line',
            data: [194, 199, 178, 116, 127, 131, 354,
                   1278, 1847, 2160, 2022, 1917, 1927,
                   1641, 1831, 1819, 1833, 2174, 1764,
                   1576, 1310, 1183, 930, 632],
            markPoint: {
                data: [
                    {type: 'max', name: '最大值'},
                    {type: 'min', name: '最小值'}
                ]
            }
        },
        {
            name: 'seqGridOutFlow',
            type: 'line',
            data: [387, 242, 202, 147, 145, 152, 423,
                   1456, 2035, 2317, 2071, 1934, 1950,
                   1666, 1815, 1833, 1832, 2152,
                   1748, 1496, 1237, 1089, 807, 354],
            markPoint: {
                data: [
                    {type: 'max', name: '最大值'},
                    {type: 'min', name: '最小值'}
                ]
            }

        },
        {
            name: 'seqGridFlow',
            type: 'line',
            data: [488, 296, 240, 168, 163, 170, 523,
                   2064, 2805, 3257, 3022, 2751, 2831,
                   2397, 2583, 2646, 2671, 3448, 2661,
                   2102, 1799, 1616, 1272, 838],
            markPoint: {
                data: [
                    {type: 'max', name: '最大值'},
                    {type: 'min', name: '最小值'}
                ]
            }

        }

    ]
};
