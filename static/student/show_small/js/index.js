// 立即执行函数，防止变量污染 (function() {})();



// main head
(function () {
  $.ajax({
    url: '/api/completion_statistics',  // 使用我们新创建的API接口
    method: 'GET',
    dataType: 'json',
    success: function(data) {
        // 更新完成和未完成的数据显示
        $('#data1').text(data.completed);
        $('#data2').text(data.notCompleted);
    },
    error: function(xhr, status, error) {
        console.error('获取数据时出错:', error);
        // 处理错误，显示错误提示
        $('#data1').text('获取失败');
        $('#data2').text('获取失败');
    }
  });
})();





// 各院系在校生参测率
// main body
(function () {
  var myChart = echarts.init(document.querySelector('.map .chart1'));

  // 定义颜色数组
  var colors = ['#3282b8', '#66bb6a', '#ff9800', '#9c27b0', '#e57373', '#00bcd4', '#8bc34a', '#f44336', '#03a9f4', '#9e9e9e', '#ff5722', '#607d8b', '#4caf50', '#f06292', '#2196f3', '#795548', '#ffc107', '#3f51b5', '#009688', '#cddc39', '#f57c00', '#81d4fa', '#f50057', '#673ab7', '#455a64', '#7e57c2', '#00e676', '#90a4ae', '#ff8a80', '#0091ea', '#82b1ff', '#4db6ac', '#d1c4e9', '#00b0ff', '#b2dfdb', '#000000'];

  // 从接口获取数据
  function fetchData() {
    $.ajax({
      url: '/api/college_participation_rate',
      method: 'GET',
      dataType: 'json',
      success: function(response) {
        var data = response.data;
        
        var option = {
          title: {
            // text: '各院系在校生参测率',
            left: '36%',
            textStyle: {
              color: "#FFFFFF"
            },
          },
          xAxis: {
            type: 'value',
            axisLabel: {
              textStyle: {
                color: '#FFFFFF'
              }
            },
          },
          grid: {
            top: 48,
            left: 155,
            right: 50,
            bottom: 50,
          },
          yAxis: {
            type: 'category',
            data: data.map(item => item.name),
            axisLabel: {
              textStyle: {
                color: '#FFFFFF'
              }
            },
          },
          series: [{
            name: '参测率',
            type: 'bar',
            data: data.map(item => item.value),
            label: {
              show: true,
              position: 'insideRight',
              formatter: '{c}%',  // 添加百分号
              color: '#FFFFFF'
            },
            itemStyle: {
              color: function(params) {
                return colors[params.dataIndex % colors.length];  // 使用取模运算确保不会超出颜色数组范围
              }
            }
          }]
        };

        myChart.setOption(option);
      },
      error: function(xhr, status, error) {
        console.error('获取数据失败:', error);
      }
    });
  }

  // 初次加载数据
  fetchData();

  // 让图表随屏幕自适应
  window.addEventListener('resize', function() {
    myChart.resize();
  });
})();




// 柱状图1
// 各年级成绩分布对比
// 11
(function () {
  var myChart = echarts.init(document.querySelector('.bar .chart'));
  
  // 定义一个函数从接口获取数据
  function fetchData() {
    $.ajax({
      url: '/api/grade_score_distribution',
      method: 'GET',
      dataType: 'json',
      success: function (response) {
        var data = response.data;
        var option = {
          color: ['#FF0000', '#ffff00', '#00FA9A', '#0096ff'],
          legend: {
            data: ['优秀', '良好', '及格', '不及格'],
            textStyle: {
              color: '#ffffff'
            },
            left: 'center',
            top: '8%',
            padding: [5, 10]
          },
          xAxis: {
            type: 'value',
            name: '',
            textStyle: {
              color: '#ffffff'
            }
          },
          yAxis: {
            type: 'category',
            data: ['大一', '大二', '大三', '大四'],
            textStyle: {
              color: '#ffffff'
            }
          },
          series: [
            {
              name: '优秀',
              type: 'bar',
              data: data['优秀'],
              stack: '总量'
            },
            {
              name: '良好',
              type: 'bar',
              data: data['良好'],
              stack: '总量'
            },
            {
              name: '及格',
              type: 'bar',
              data: data['及格'],
              stack: '总量'
            },
            {
              name: '不及格',
              type: 'bar',
              data: data['不及格'],
              stack: '总量'
            }
          ],
          barWidth: 8,
          textStyle: {
            color: '#ffffff'
          }
        };

        myChart.setOption(option);
      },
      error: function (xhr, status, error) {
        console.error('获取数据失败:', error);
      }
    });
  }

  // 初次加载数据
  fetchData();

  // 让图表随屏幕自适应
  window.addEventListener('resize', function () {
    myChart.resize();
  });
})();





// 柱状图2
//不同群体体测平均成绩
// 12
(function () {
  var myChart = echarts.init(document.querySelector(".bar2 .chart"));
  
  var option = {
    color: ['#2f89cf'],
    tooltip: {
      trigger: 'axis',
      formatter: '{b}<br/>平均成绩: {c}分<br/>'
    },
    grid: {
      left: '0%',
      top: '10px',
      right: '0%',
      bottom: '4%',
      containLabel: true
    },
    xAxis: [{
      type: 'category',
      data: [],
      axisLabel: {
        color: "rgba(255,255,255,0.8)",
        fontSize: 10,
        interval: 0,
        rotate: 0
      },
      axisLine: { show: false }
    }],
    yAxis: [{
      type: 'value',
      name: '平均成绩',
      min: 0,
      max: 100,
      interval: 20,
      nameTextStyle: {
        color: "rgba(255,255,255,0.8)",
        fontSize: 12
      },
      axisLabel: {
        color: "rgba(255,255,255,0.6)",
        fontSize: 12,
        formatter: '{value}分'
      },
      splitLine: {
        lineStyle: { color: "rgba(255,255,255,0.1)" }
      }
    }],
    series: [{
      name: '平均成绩',
      type: 'bar',
      barWidth: '35%',
      data: [],
      itemStyle: { 
        barBorderRadius: 5,
        color: function(params) {
          // 根据分数设置不同的颜色
          var value = params.value;
          if (value >= 90) return '#67C23A';  // 优秀
          if (value >= 80) return '#409EFF';  // 良好
          if (value >= 70) return '#E6A23C';  // 中等
          if (value >= 60) return '#F56C6C';  // 及格
          return '#909399';  // 不及格
        }
      }
    }]
  };

  function loadData() {
    $.ajax({
      url: '/api/cluster_analysis_result',
      type: 'GET',
      success: function(res) {
        if (res && res.success && res.data && Array.isArray(res.data.clusterStats)) {
          var clusterStats = res.data.clusterStats;
          option.xAxis[0].data = clusterStats.map(item => item.name);
          option.series[0].data = clusterStats.map(item => ({
            value: item.value || 0,
            count: item.count || 0
          }));
          myChart.setOption(option);
        } else {
          showError('数据加载失败', res ? res.msg : '未知错误');
        }
      },
      error: function() {
        showError('数据加载失败', '请检查网络连接');
      }
    });
  }

  function showError(title, subtext) {
    myChart.setOption({
      title: {
        text: title,
        subtext: subtext,
        left: 'center',
        top: 'center',
        textStyle: { color: '#fff' }
      }
    });
  }

  loadData();
  window.addEventListener('resize', () => myChart.resize());
  setInterval(loadData, 5 * 60 * 1000);
})();












// 折线图1
// 各年级平均BMI
// 21
(function () {
  var myChart = echarts.init(document.querySelector(".line .chart"));

  // 定义一个函数从接口获取数据
  function fetchData() {
    $.ajax({
      url: '/api/average_bmi_data', // 替换为你的实际接口地址
      method: 'GET',
      dataType: 'json',
      success: function (response) {
        // 假设返回的数据结构为 { data: { bmi: [...], weight: [...], height: [...] } }
        var yearData = response.data;
        var option = {
          // 修改两条线的颜色
          color: ['#00f2f1', '#ed3f35', '#FFA500'],
          tooltip: {
            trigger: 'axis'
          },
          // 图例组件
          legend: {
            textStyle: {
              color: '#4c9bfd'
            },
            right: '10%',
          },
          grid: {
            top: "20%",
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true,
            show: true,
            borderColor: '#012f4a'
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: ['大一', '大二', '大三', '大四'],
            axisTick: {
              show: false
            },
            axisLabel: {
              color: "#4c9bfb"
            },
            axisLine: {
              show: false
            }
          },
          yAxis: {
            type: 'value',
            axisTick: {
              show: false
            },
            axisLabel: {
              color: "#4c9bfb"
            },
            axisLine: {
              show: false
            },
            splitLine: {
              lineStyle: {
                color: "#012f4a"
              }
            }
          },
          series: [{
            type: 'line',
            smooth: true,
            name: '平均BMI',
            data: yearData.bmi
          },
          {
            type: 'line',
            smooth: true,
            name: '平均体重',
            data: yearData.weight
          },
          {
            type: 'line',
            smooth: true,
            name: '平均身高',
            data: yearData.height
          }
          ]
        };

        myChart.setOption(option);
      },
      error: function (xhr, status, error) {
        console.error('获取数据失败:', error);
      }
    });
  }

  // 初次加载数据
  fetchData();

  // 让图表随屏幕自适应
  window.addEventListener('resize', function () {
    myChart.resize();
  });
})();






// 折线图2
// 体测成绩时间序列趋势
// 22
(function () {
  var myChart = echarts.init(document.querySelector('.line2 .chart'));

  // 从后端获取数据
  $.ajax({
    url: '/api/single_day_test_count_data_statistics',
    type: 'GET',
    success: function(res) {
      if (res.success) {
        var dates = res.data.dates;
        var counts = res.data.counts;
        
        // 格式化日期显示
        var formattedDates = dates.map(date => {
          var parts = date.split('-');
          return parts[1]; // 只显示月份数字
        });

        var option = {
          tooltip: {
            trigger: 'axis',
            formatter: function(params) {
              var date = dates[params[0].dataIndex];
              return date + '<br/>体测人数: ' + params[0].value;
            }
          },
          legend: {
            top: "0%",
            textStyle: {
              color: "rgba(255,255,255,.5)",
              fontSize: "12"
            }
          },
          grid: {
            top: '30',
            left: '10',
            right: '30',
            bottom: '10',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            axisLabel: {
              color: "rgba(255,255,255,.6)",
              fontSize: 12,
              interval: function(index, value) {
                // 只显示每个月的第一天
                var date = dates[index];
                return date.split('-')[2] === '01';
              },
              rotate: 0 // 不旋转标签
            },
            axisLine: {
              lineStyle: {
                color: "rgba(255,255,255,.2)"
              }
            },
            data: formattedDates
          },
          yAxis: {
            type: 'value',
            axisTick: { show: false },
            axisLine: {
              lineStyle: {
                color: "rgba(255,255,255,.1)"
              }
            },
            axisLabel: {
              color: "rgba(255,255,255,.6)",
              fontSize: 12
            },
            splitLine: {
              lineStyle: {
                color: "rgba(255,255,255,.1)"
              }
            }
          },
          series: [{
            name: '体测日期',
            type: 'line',
            smooth: true,
            lineStyle: {
              color: "#0184d5",
              width: 2
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: "rgba(1, 132, 213, 0.4)" },
                { offset: 0.8, color: "rgba(1, 132, 213, 0.1)" }
              ])
            },
            symbol: 'circle',
            symbolSize: 5,
            showSymbol: false,
            itemStyle: {
              color: "#0184d5"
            },
            data: counts
          }]
        };

        myChart.setOption(option);
      }
    },
    error: function(err) {
      console.error('获取体测数据失败:', err);
    }
  });

  window.addEventListener('resize', function () {
    myChart.resize();
  });
})();














// 饼形图1
//实测成绩分布
// 31
(function () {
  // 定义一个异步函数来获取数据
  $.ajax({
    url: '/api/distribution_of_actual_test_scores', // 修改为相对路径
    type: 'GET',
    dataType: 'json',
    success: function (data) {
      final_data = data.data; // 将返回的数据存储到 final_data 变量中
      var myChart = echarts.init(document.querySelector(".pie .chart"));
      var option = {
        color: ["#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6"],
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          // 垂直居中,默认水平居中
          // orient: 'vertical',

          bottom: 0,
          left: 10,
          // 小图标的宽度和高度
          itemWidth: 10,
          itemHeight: 10,
          // 修改图例组件的文字为 12px
          textStyle: {
            color: "rgba(255,255,255,.5)",
            fontSize: "10"
          }
        },
        series: [{
          name: '成绩',
          type: 'pie',
          // 设置饼形图在容器中的位置
          center: ["50%", "42%"],
          // 修改饼形图大小，第一个为内圆半径，第二个为外圆半径
          radius: ['40%', '60%'],
          avoidLabelOverlap: false,
          // 图形上的文字
          label: {
            show: false,
            position: 'center'
          },
          // 链接文字和图形的线
          labelLine: {
            show: false
          },
          data: final_data
        }]
      };

      myChart.setOption(option);
      window.addEventListener('resize', function () {
        myChart.resize();
      })
    }
  });
})();





// 饼形图2
// 体测数据异常值占比
(function () {
  var myChart = echarts.init(document.querySelector('.pie2 .chart'));
  
  // 获取异常统计数据
  fetch('/api/error_statistics')
    .then(response => response.json())
    .then(data => {
      var option = {
        color: ['#60cda0', '#ed8884', '#ff9f7f', '#0096ff', '#9fe6b8', '#32c5e9', '#1d9dff'],
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
          bottom: 0,
          itemWidth: 10,
          itemHeight: 10,
          textStyle: {
            color: "rgba(255,255,255,.5)",
            fontSize: 10
          }
        },
        series: [{
          name: '异常类型分布',
          type: 'pie',
          radius: ["10%", "60%"],
          center: ['50%', '40%'],
          roseType: 'radius',
          label: {
            fontSize: 10
          },
          labelLine: {
            length: 6,
            length2: 8
          },
          data: data.data
        }]
      };

      myChart.setOption(option);
    })
    .catch(error => console.error('Error fetching error statistics:', error));

  window.addEventListener('resize', function () {
    myChart.resize();
  });
})();



