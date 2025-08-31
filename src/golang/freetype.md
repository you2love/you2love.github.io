# freetype

```golang
package main

import (
 "fmt"
 "image"
 "image/draw"
 "image/png"
 "os"
 "github.com/golang/freetype"
)

func DrawText(text string) {
 data, err := ioutil.ReadFile("/System/Library/Fonts/STHeiti Medium.ttc")
 if err != nil {
  panic(err)
 }
 f, err := freetype.ParseFont(data)
 if err != nil {
  panic(err)
 }

 dst := image.NewRGBA(image.Rect(0, 0, 800, 600))
 draw.Draw(dst, dst.Bounds(), image.White, image.Point{}, draw.Src)

 c := freetype.NewContext()
 c.SetDst(dst)
 c.SetClip(dst.Bounds())
 c.SetSrc(image.Black)
 c.SetFont(f)
 fontSize := float64(50)
 // 字体越大, 显示越大
 c.SetFontSize(fontSize)

 // Pt是控制起点,Pt{x,y},x表示左起点,y表示下起点,y-fontSize才是上起点
 _, err = c.DrawString(text, freetype.Pt(0, int(fontSize)))
 if err != nil {
  panic(err)
 }

 pngFile, err := os.Create("draw.png")
 if err != nil {
  panic(err)
 }
 defer pngFile.Close()

 err = png.Encode(pngFile, dst)
 if err != nil {
  panic(err)
 }
}

func main() {
 DrawText("中国人golang语言教程ABC122")
}
```
