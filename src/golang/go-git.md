---
# go-git
---

```golang

package main

import(
    "fmt"
    "github.com/go-git/go-git/v5"
    "github.com/go-git/go-git/v5/plumbing/object"
)
 

func gitWork() {
 r, err := git.PlainOpen("../wubei/wubei")
 if err != nil {
  fmt.Println(err)
  return
 }

 fmt.Println("r", r)

 // ... retrieves the branch pointed by HEAD
 ref, err := r.Head()
 if err != nil {
  fmt.Println(err)
  return
 }

 fmt.Println("ref", ref)

 // ... retrieves the commit history
 cIter, err := r.Log(&git.LogOptions{From: ref.Hash()})
 if err != nil {
  fmt.Println(err)
  return
 }

 var cCount int
 err = cIter.ForEach(func(c *object.Commit) error {
  cCount++
  fmt.Println("Author", c.Author)
  fmt.Println("Message", c.Message)
  return nil
 })
 if err != nil {
  fmt.Println(err)
  return
 }

 fmt.Println("cCount", cCount)
}
```
