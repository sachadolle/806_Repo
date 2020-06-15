create database solutions;
use publications;

## challenge 1

select authors.au_id as 'AUTHOR ID', au_lname as 'LAST NAME', au_fname as 'FIRST NAME', title as TITLE, pub_name as PUBLISHER 
from authors authors
inner join titleauthor titleauthor on titleauthor.au_id=authors.au_id
inner join titles titles on titles.title_id=titleauthor.title_id
inner join publishers publishers on publishers.pub_id=titles.pub_id
order by authors.au_id asc
;

##Challenge 2

select authors.au_id as 'AUTHOR ID', au_lname as 'LAST NAME', au_fname as 'FIRST NAME', pub_name as PUBLISHER, count(titles.title) as TITLE_COUNT
from authors authors
inner join titleauthor titleauthor on titleauthor.au_id=authors.au_id
inner join titles titles on titles.title_id=titleauthor.title_id
inner join publishers publishers on publishers.pub_id=titles.pub_id
group by authors.au_id, publishers.pub_name
order by TITLE_COUNT desc;

## Challenge 3
select authors.au_id as 'AUTHOR ID', authors.au_lname as 'LAST NAME', authors.au_fname as 'FIRST NAME', count(qty) as TOTAL
from authors authors 
inner join titleauthor titleauthor on titleauthor.au_id=authors.au_id
inner join sales s on s.title_id=titleauthor.title_id
group by authors.au_id
order by TOTAL desc
limit 3;

## Challenge 4

select authors.au_id as 'AUTHOR ID', authors.au_lname as 'LAST NAME', authors.au_fname as 'FIRST NAME', ifnull(sum(titles.ytd_sales), 0) as TOTAL
from authors authors 
inner join titleauthor titleauthor on titleauthor.au_id=authors.au_id
inner join titles titles on titles.title_id=titleauthor.title_id
group by authors.au_id
order by TOTAL desc
;