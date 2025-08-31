# unity
<!-- toc --> 

### 清除启动界面工程

```bash
cd /Users/<yourUserName>/Library/Preferences/

cat com.unity3d.UnityEditor5.x.plist

defaults read com.unity3d.UnityEditor5.x.plist
defaults delete com.unity3d.UnityEditor5.x "RecentlyUsedProjectPaths-0"
```

### 打印调用堆栈

```c#
string trackStr = new System.Diagnostics.StackTrace().ToString();
Debug.Log ("Stack Info:" + trackStr);
```

### 积累

1. Unity是单线程设计的游戏引擎,子线程中无法运行Unity SDK
2. Unity主循环是单线程,游戏脚本MonoBehavior有着严格的生命周期
3. 倾向使用time slicing（时间分片）的协程（coroutine）去完成异步任务

### 组件图

![组件图](/webp/unity/component.webp "组件图")

### 常见热更方案

#### 利用c#反射,动态加载程序集,实现代码更新

```c#
// 从指定网址下载
Assembly assembly = Assembly.LoadFile(assemblyFile);
```

#### 创建Lua虚拟机,动态加载Lua脚本

 1. [腾讯-xLua方案](https://github.com/Tencent/xLua)

    ```c#
    XLua.LuaEnv luaenv = new XLua.LuaEnv();
    luaenv.DoString("CS.UnityEngine.Debug.Log('hello world')");
    luaenv.Dispose();
    ```

 2. [tolua-号称最快](https://github.com/topameng/tolua)

    ```C#
    LuaState lua = new LuaState();
    lua.Start();
    lua.DoString("print('hello world')");
    lua.Dispose();
    ```
