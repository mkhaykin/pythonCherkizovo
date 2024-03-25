:setvar db_name TestDB
:setvar user_uid db_user
:setvar user_pwd Q1q

USE [master]
GO

CREATE LOGIN [$(user_uid)] WITH PASSWORD=N'$(user_pwd)', DEFAULT_DATABASE=[master], CHECK_EXPIRATION=OFF, CHECK_POLICY=OFF
GO

IF DB_ID('TestDB') IS NOT NULL
  set noexec on

CREATE DATABASE [$(db_name)]
GO

USE [TestDB];
GO

ALTER AUTHORIZATION ON DATABASE::[$(db_name)] TO [$(user_uid)]
GO

CREATE TABLE [dbo].[sales](
	[dt] [date] NOT NULL,
	[article] [varchar](50) NOT NULL,
	[kg] [int] NOT NULL
) ON [PRIMARY]
GO

CREATE PROCEDURE [dbo].[sp_test] (
	@dt_from Date,
	@dt_to Date
) AS
BEGIN
	SET NOCOUNT ON;

    WITH month_sales AS (
        SELECT
            YEAR(dbo.sales.dt) as _year,
            MONTH(dbo.sales.dt) as _month,
            dbo.sales.article as article,
            SUM(dbo.sales.kg) as sum_kg
        FROM dbo.sales
        GROUP BY YEAR(dbo.sales.dt),
            MONTH(dbo.sales.dt),
            dbo.sales.article
    ), avg_month_sales AS (
        SELECT
            month_sales._year,
            month_sales.article,
            avg(sum_kg) as avg_kg
        FROM month_sales
        GROUP BY _year,
            article
    ), year_sales AS (
        SELECT
            YEAR(_year) as _year,
            month_sales.article,
            SUM(sum_kg) as sum_kg
        FROM month_sales
        GROUP BY
            YEAR(_year),
            article
    ), avg_year_sales AS (
        SELECT
            year_sales.article,
            AVG(sum_kg) as avg_kg
        FROM year_sales
        GROUP BY
            article
    ), period_sales AS (
            SELECT
                YEAR(dbo.sales.dt) as _year,
                MONTH(dbo.sales.dt) as _month,
                dbo.sales.article,
                SUM(dbo.sales.kg) as sum_kg
            FROM
                dbo.sales
            WHERE
                dt BETWEEN @dt_from AND @dt_to
            GROUP BY
                YEAR(dbo.sales.dt),
                MONTH(dbo.sales.dt),
                dbo.sales.article
        )
    SELECT
        period_sales._year,
        period_sales._month,
        period_sales.article,
        period_sales.sum_kg as saled_by_period,
        avg_year_sales.avg_kg as year_avg_sale,
        ROUND(1.0 * period_sales.sum_kg / avg_year_sales.avg_kg, 2) as share_by_year,
        avg_month_sales.avg_kg as month_avg_sale,
        ROUND(1.0 * period_sales.sum_kg / avg_month_sales.avg_kg, 2) as share_by_month
    FROM period_sales
        INNER JOIN avg_year_sales ON period_sales.article = avg_year_sales.article
        INNER JOIN avg_month_sales ON period_sales.article = avg_month_sales.article AND period_sales._year = avg_month_sales._year
    ORDER BY 1, 2, 3
END
GO
