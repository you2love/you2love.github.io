# log
<!-- toc --> 


### 日志常用示例

```golang
package main

import (
 "fmt"
 "io"
 "io/ioutil"
 "runtime"
 "strings"
 "time"

 rotatelogs "github.com/lestrrat-go/file-rotatelogs"
 "github.com/rifflock/lfshook"
 "github.com/sirupsen/logrus"
)

func NewWriter(perfix string) io.Writer {
 w, err := rotatelogs.New(
  perfix+".%Y%m%d.json",
  // 建立软接
  rotatelogs.WithLinkName(perfix),
  // 最多保存一星期
  rotatelogs.WithMaxAge(7*24*time.Hour),
  // 一天切割一次
  rotatelogs.WithRotationTime(24*time.Hour),
 )
 if err != nil {
  panic(err)
 }
 return w
}

func InitLog(perfix string) {
 wm := lfshook.WriterMap{
  logrus.DebugLevel: NewWriter(perfix + "_debug"),
  logrus.InfoLevel:  NewWriter(perfix + "_info"),
  logrus.WarnLevel:  NewWriter(perfix + "_warn"),
  logrus.ErrorLevel: NewWriter(perfix + "_error"),
  logrus.FatalLevel: NewWriter(perfix + "_fatal"),
 }
 logrus.AddHook(lfshook.NewHook(
  wm,
  &logrus.JSONFormatter{
   CallerPrettyfier: func(f *runtime.Frame) (string, string) {
    var callerName, fileName string
    names := strings.SplitAfterN(f.File, perfix, 2)
    if len(names) > 1 {
     fileName = fmt.Sprintf("%v;%v", names[1], f.Line)
    }

    names = strings.SplitAfterN(f.Function, perfix, 2)
    if len(names) > 1 {
     callerName = names[1]
    } else {
     callerName = f.Function
    }

    return callerName, fileName
   },
   PrettyPrint: true,
  },
 ))

 logrus.SetOutput(ioutil.Discard)
 logrus.SetReportCaller(true)
 logrus.SetLevel(logrus.InfoLevel)

 logrus.WithFields(logrus.Fields{
  "perfix": perfix,
  "level":  logrus.GetLevel(),
 }).Warn("日志初始化完成")
}
```
