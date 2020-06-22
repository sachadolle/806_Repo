use publications;

	#CHALLENGE 1

# Step 1
select t.title_id as Title_ID, ta.au_id as Author_ID, t.advance*ta.royaltyper/100 as Advance,
t.price * s.qty * t.royalty / 100 * ta.royaltyper / 100 as sales_royalty
from titleauthor ta
inner join titles t on t.title_id=ta.title_id
inner join sales s on s.title_id=ta.title_id
;

# Step 2
select Title_ID, Author_ID, sum(sales_royalty)
from 
	(select t.title_id as Title_ID, ta.au_id as Author_ID, t.advance*ta.royaltyper/100 as Advance, t.price * s.qty * t.royalty / 100 * ta.royaltyper / 100 as sales_royalty
	from titleauthor ta
	inner join titles t on t.title_id=ta.title_id
	inner join sales s on s.title_id=ta.title_id
) summary
group by Title_ID, Author_ID
;

# Step 3
select summary1.Title_ID, summary1.Author_ID, (sales_royalty + total_Advance) as Profits
from 
	(select t.title_id as Title_ID, ta.au_id as Author_ID, t.advance*ta.royaltyper/100 as Advance, t.price * s.qty * t.royalty / 100 * ta.royaltyper / 100 as sales_royalty
	from titleauthor ta
	inner join titles t on t.title_id=ta.title_id
	inner join sales s on s.title_id=ta.title_id    
	) summary1
inner join
	(select t.title_id, ifnull(sum(t.advance), 0) as total_Advance
    from titles t
    group by title_id
    ) summary2
group by Title_ID, Author_ID
order by Profits desc
limit 3
;


	#CHALLENGE 2

CREATE TEMPORARY TABLE publications.temp1
select t.title_id as Title_ID, ta.au_id as Author_ID, t.advance*ta.royaltyper/100 as Advance, t.price * s.qty * t.royalty / 100 * ta.royaltyper / 100 as sales_royalty
from titleauthor ta
inner join titles t on t.title_id=ta.title_id
inner join sales s on s.title_id=ta.title_id;

CREATE TEMPORARY TABLE publications.temp2
select t.title_id, ifnull(sum(t.advance), 0) as total_Advance
from titles t
group by title_id;
 
CREATE TEMPORARY TABLE publications.temp3
select temp1.Title_ID, temp1.Author_ID, (sales_royalty + total_Advance) as Profits
from temp1
inner join temp2
group by Title_ID, Author_ID
order by Profits desc
limit 3
;

		#CHALLENGE 3

CREATE TABLE most_profiting_authors (
	Author_ID VARCHAR(11),
	profits FLOAT
);

insert into most_profiting_authors (Author_ID, profits) 
select Author_ID, Profits
from temp3
;

select * from most_profiting_authors;