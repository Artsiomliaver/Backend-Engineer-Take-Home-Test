# Backend-Engineer-Take-Home-Test
Backend Engineer Take Home Test
# Prompt

### Introduction

Please only spend 2-4 hours on this. We are interested in the code design and the choices you make. Any works that make the code better (especially when you work in a team) are also welcomed. If you run out of time, please include a document outlining how you would finish. 

Restrictions:

- Choose any programming language other than bash.
- Do not invoke unix utilities (i.e. curl, wget, etc)

### Problem

Please implement a command line program that can fetch web pages and saves them to disk for later retrieval and browsing.

**Section 1**

For example if we invoked your program like this: `./fetch [https://www.google.com](https://www.google.com)` then in our current directory we should have a file containing the contents of `www.google.com`. (i.e. `/home/myusername/fetch/www.google.com.html`).

We should be able to specify as many urls as we want:

```jsx
$> ./fetch https://www.google.com https://autify.com <...>
$> ls
autify.com.html www.google.com.html
```

If the program runs into any errors while downloading the html it should print the error to the console.

**Section 2**

Record metadata about what was fetched:

- What was date and time of last fetch
- How many links are on the page
- How many images are on the page

Modify the script to print this metadata.

For example (it can work differently if you like)

```jsx
$> ./fetch --metadata https://www.google.com
site: www.google.com
num_links: 35
images: 3
last_fetch: Tue Mar 16 2021 15:46 UTC
```

### Extra credit (only if you have time)

Archive all assets as well as html so that you load the web page locally with all assets loading properly.
